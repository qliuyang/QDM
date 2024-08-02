import json
import time
from hashlib import sha256
from pathlib import Path
from typing import Dict, List, Tuple

import requests
from PySide6.QtCore import QThread, Signal, QFileInfo, QMutex, QObject, Qt
from PySide6.QtWidgets import QFileIconProvider, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, \
    QMenu, QListWidget, QListWidgetItem
from qfluentwidgets import ProgressBar
from qframelesswindow import FramelessWindow
from Ui_MoreInfo import Ui_Form as MoreInfoForm
from config import Config, Style


def convertBytes(byte) -> Tuple[float, str]:
    mb = round(byte / (1024 * 1024), 2)
    if mb >= 1:
        return mb, "MB"
    kb = round(byte / (1024 * 1024), 2)
    if kb >= 1:
        return kb, "KB"
    return byte, "B"


class State(QObject):
    updateState = Signal(object)

    def __init__(self, stateDict: Dict):
        super().__init__()
        self._stateDict = stateDict
        self._state = ''

    @property
    def rawState(self):
        return self._state

    @property
    def uiState(self):
        return self._stateDict.get(self._state)

    @rawState.setter
    def rawState(self, value):
        self._state = value
        self.updateState.emit(self)


class Progress(QObject):
    updateProgress = Signal(object)

    def __init__(self, progress: float):
        super().__init__()
        self._progress = progress

    @property
    def progress(self) -> int:
        return int(self._progress)

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.updateProgress.emit(self)


class Speed(QObject):
    updateSpeed = Signal(object)

    def __init__(self, speed: float):
        super().__init__()
        self._speed = speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value
        self.updateSpeed.emit(self)


class Error(QObject):
    updateError = Signal(object)

    def __init__(self):
        super().__init__()

        self.statusCode = None
        self.msg = None

    def build(self, msg: str = None, statusCode: int = None):
        self.msg = msg
        self.statusCode = statusCode


class FileInfo:
    def __init__(self, state: State):
        super().__init__()

        self.url = None
        self.state = state
        self.fileName = ''
        self.fileSize = 0
        self.error = Error()

    @property
    def info(self):
        return {
            "fileName": self.fileName,
            "fileSize": self.fileSize,
            "url": self.url
        }

    def loadUrl(self, url):
        self.url = url

    def loadDownloadInfo(self, fileInfo: Dict):
        self.fileName = fileInfo['fileName']
        self.fileSize = fileInfo['fileSize']
        self.url = fileInfo['url']

    def buildHeader(self):
        self.state.rawState = "WAITING_STATE"
        try:
            header = requests.head(self.url, timeout=5)
        except requests.exceptions.ConnectTimeout:
            self.error.build("连接超时", 504)
        except requests.exceptions.ReadTimeout:
            self.error.build("读取超时", 504)
        except requests.exceptions.TooManyRedirects:
            self.error.build("重定向次数过多", 310)
        except requests.exceptions.RequestException:
            self.error.build("连接失败", 500)
        else:
            if header.is_redirect:
                # 获取重定向Url
                self.url = header.headers.get('Location', self.url)
                # 重定向后的Url
                header = requests.head(self.url)

            self.fileSize = int(header.headers.get('Content-Length', 0))
            self.fileName = self.url.split('/')[-1]


class Downloader(QThread):
    """
    新的下载: wait -> ready -> downloading -> completed
    暂停后继续下载: wait -> ready -> downloading -> pause -> wait -> ready -> downloading -> completed
    加载链接错误: wait -> error
    """

    def __init__(self, config: Config):
        super().__init__()
        self.endPos = None
        self.startPos = None

        self._downloadInfo = None
        self._config = config
        self._downloadConfig = config.getDownloadConfig()

        self.state = State(config.getStateConfig())
        self.progress = Progress(0)
        self.speed = Speed(0)

        self._fileInfo = FileInfo(self.state)

        self._fileIcon = None
        self._outputPath = None
        self._tempPath = None
        self._outputFile = None
        self._fileType = None
        self._downloadInfoFile = None
        self._downloadInfoPath = None
        self._fileChunkNum = 1024
        self._isStop = False
        self.mode = None

    def initDownload(self):
        self._fileType = self.getDownloadFileType()

        self._downloadInfoPath = Path(self._downloadConfig['downloadInfoPath'])
        self._downloadInfoFile = self._downloadInfoPath / f"{self._fileInfo.fileName}.json"

        self._tempPath = Path(self._downloadConfig['tempPath'])

        self._outputPath = Path(self._downloadConfig['output']) / self._fileType
        self._outputFile = self._outputPath / self._fileInfo.fileName

        self._outputPath.mkdir(parents=True, exist_ok=True)
        self._downloadInfoPath.mkdir(parents=True, exist_ok=True)
        self._tempPath.mkdir(parents=True, exist_ok=True)

        self.makeEmptyFile(self._outputFile)

        self._fileIcon = self.getFileIcon()

        self.state.rawState = "READY_STATE"

    @staticmethod
    def makeEmptyFile(file: Path):
        if not file.is_file():
            with open(file, "w+"):
                pass

    def run(self):
        self.mode()

    def continueDownload(self):
        downloadRanges = self._downloadInfo['downloadRanges']
        if downloadRanges:
            self.download(downloadRanges)

    def creatPauseDownload(self, downloadInfo: Dict):
        self._downloadInfo = downloadInfo
        self._fileInfo.loadDownloadInfo(downloadInfo['fileInfo'])

        self.initDownload()

        self.progress.progress = downloadInfo['progress']
        self.state.rawState = downloadInfo['state']

    def creatNewDownload(self, url: str):
        self._fileInfo.loadUrl(url)
        self._fileInfo.buildHeader()
        error = self._fileInfo.error

        if error.msg and error.statusCode:
            self.state.rawState = "ERROR_STATE"
            error.updateError.emit(error)
            return

        self.initDownload()
        downloadRanges = [0, self._fileInfo.fileSize]
        self.download(downloadRanges)

    @property
    def fileInfo(self):
        return self._fileInfo

    @property
    def fileType(self):
        return self._fileType

    @property
    def fileIcon(self):
        return self._fileIcon

    def getFileIcon(self):
        extension = Path(self._fileInfo.fileName).suffix
        tempFile = Path(f"{sha256(extension.encode()).hexdigest()}{extension}")
        tempFilePath = self._tempPath / tempFile

        self.makeEmptyFile(tempFilePath)

        file_info = QFileInfo(tempFile)
        icon_provider = QFileIconProvider()

        return icon_provider.icon(file_info).pixmap(29, 29)

    def getDownloadFileType(self) -> str:
        fileType = self._downloadConfig['fileType']
        fileExtension = Path(self._fileInfo.fileName).suffix[1:].lower()
        for category, extensions in fileType.items():
            if fileExtension in extensions:
                return category

    def saveDownloadInfo(self, downloadRanges: List = None):
        self._downloadInfo = {
            'fileInfo': self._fileInfo.info,
            'state': self.state.rawState,
            'progress': self.progress.progress,
            'downloadRanges': downloadRanges
        }
        if not self._downloadInfoFile:
            return
        with open(self._downloadInfoFile, "w") as f:
            json.dump(self._downloadInfo, f)

    def calcTheDownloadProgress(self, finishedDownload):
        return round(finishedDownload / self._fileInfo.fileSize * 100, 2)

    def quit(self):
        self.stopDownload()
        self.clearDownloadInfo()
        super().quit()

    def clearDownloadInfo(self):
        if self._downloadInfoFile:
            self._downloadInfoFile.unlink()

    def stopDownload(self):
        self.state.rawState = "PAUSE_STATE"
        self.saveDownloadInfo(downloadRanges=[self.startPos, self.endPos])
        self._isStop = False

    def download(self, ranges: List):
        self.startPos, self.endPos = ranges

        self.state.rawState = 'DOWNLOADING_STATE'
        res = requests.get(self._fileInfo.url, headers={'Range': f'bytes={str(int(self.startPos))}-{str(self.endPos)}'},
                           stream=True)
        statTime = time.time()
        with open(self._outputFile, 'r+b') as f:
            tempSize = 0

            for chunk in res.iter_content(self._fileChunkNum):
                f.seek(self.startPos)
                f.write(chunk)

                if self._isStop:
                    self.stopDownload()
                    return

                self.startPos += len(chunk)
                if time.time() - statTime > 1:
                    statTime = time.time()
                    speed = self.startPos - tempSize
                    self.speed.speed = speed
                    tempSize = self.startPos

                oneIter = self.calcTheDownloadProgress(self.startPos)
                self.progress.progress = oneIter

        self.state.rawState = "COMPLETED_STATE"
        self.saveDownloadInfo()

    def stop(self):
        self._isStop = True

    @property
    def outputPath(self):
        return self._outputPath


class DownloadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.moreInfo = None
        self.downloader = None
        self.outerLayout = QVBoxLayout(self)
        self.innerLayout = QHBoxLayout()

        self.fileIcon = QLabel()
        self.fileNameLabel = QLabel()
        self.downloadSpeedLable = QLabel()
        self.downloadState = QLabel()

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.innerLayout.addWidget(self.fileIcon)
        self.innerLayout.addWidget(self.fileNameLabel)
        self.innerLayout.addItem(self.horizontalSpacer)
        self.innerLayout.addWidget(self.downloadSpeedLable)
        self.innerLayout.addWidget(self.downloadState)

        self.innerLayout.setSpacing(10)
        self.innerLayout.setContentsMargins(1, 5, 5, 5)

        self.downloadProgress = ProgressBar()
        self.downloadProgress.setValue(0)

        self.outerLayout.addLayout(self.innerLayout)
        self.outerLayout.addWidget(self.downloadProgress)

        self.outerLayout.setSpacing(10)
        self.outerLayout.setContentsMargins(5, 5, 5, 5)

        self.mutexProgress = QMutex()
        self.mutexState = QMutex()
        self.mutexSpeed = QMutex()

    def initDownload(self, downloader: Downloader):
        self.downloader = downloader
        self.moreInfo = MoreInfo(downloader)

    def updateProgress(self, num: Progress):
        self.mutexProgress.lock()
        self.downloadProgress.setValue(num.progress)
        self.mutexProgress.unlock()

    def updateState(self, state: State):
        self.mutexState.lock()

        if state.rawState in ("READY_STATE", "COMPLETED_STATE", "DOWNLOADING_STATE"):
            self.downloadProgress.setMaximum(100)
            self.fileNameLabel.setText(self.downloader.fileInfo.fileName)
            self.fileIcon.setPixmap(self.downloader.fileIcon)
        elif state.rawState == "WAITING_STATE":
            self.downloadProgress.setMaximum(0)
        elif state.rawState == "ERROR_STATE":
            self.downloadProgress.setMaximum(100)
            self.downloadProgress.setValue(0)
            self.fileNameLabel.setText(self.downloader.fileInfo.url)

        self.downloadState.setText(state.uiState)
        self.mutexState.unlock()

    def updateDownloadSpeed(self, speed: Speed):
        self.mutexSpeed.lock()
        speedWitUnit = convertBytes(speed.speed)
        self.downloadSpeedLable.setText(f"{str(speedWitUnit[0])} {speedWitUnit[1]}/s")
        self.mutexSpeed.unlock()


class MoreInfo(FramelessWindow, MoreInfoForm):
    def __init__(self, downloader: Downloader):
        super().__init__()
        self.setupUi(self)
        self.downloader = downloader

    def updateProgress(self, num: Progress):
        self.bigProgress.setValue(num.progress)

    def updateSpeed(self, speed: Speed):
        speedWitUnit = convertBytes(speed.speed)
        self.speedLabel.setText(f"{str(speedWitUnit[0])} {speedWitUnit[1]}/s")

    def updateState(self, state: State):
        self.stateLabel.setText(state.uiState)

    def updateError(self, error: Error):
        self.errorLabel.setText(error.msg + f" (code:{error.statusCode})")

    def setInfo(self):
        fileSizeWitUnit = convertBytes(self.downloader.fileInfo.fileSize)
        self.fileSizeLabel.setText(
            f"{self.downloader.fileInfo.fileSize} ({str(fileSizeWitUnit[0])} {fileSizeWitUnit[1]})")
        self.fileNameLabel.setText(self.downloader.fileInfo.fileName)
        self.urlLabel.setText(self.downloader.fileInfo.url)
        self.stateLabel.setText(self.downloader.state.uiState)
        self.saveLabel.setText(str(self.downloader.outputPath))


class DownloadWidgetList(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, position):
        item: QListWidgetItem = self.itemAt(position)
        if item:
            menu = QMenu(self)
            delete = menu.addAction(self.tr("Delete"))
            stop = menu.addAction(self.tr("stop"))
            continue_ = menu.addAction(self.tr("Continue"))
            moreInfo = menu.addAction(self.tr("More Information"))

            action = menu.exec_(self.mapToGlobal(position))
            widget:DownloadWidget = self.itemWidget(item)
            if action == delete:
                widget.downloader.quit()
                self.takeItem(self.row(item))
            elif action == stop:
                widget.downloader.stop()
            elif action == continue_:
                widget.downloader.continueDownload()
            elif action == moreInfo:
                widget.moreInfo.setInfo()
                widget.moreInfo.show()

    def filterItems(self, text: str):
        for i in range(self.count()):
            item = self.item(i)
            item_widget: DownloadWidget = self.itemWidget(item)
            if not item_widget:
                continue
            if text.startswith(":"):
                fileType = text[1:]
                item.setHidden(fileType in item_widget.downloader.fileType)
            else:
                item.setHidden(text not in item_widget.fileNameLabel.text())

    def addDownloadWidget(self, widget: DownloadWidget):
        listItem = QListWidgetItem(self)
        listItem.setSizeHint(widget.sizeHint())
        self.setItemWidget(listItem, widget)


class DownloadEngine:
    def __init__(self, config: Config, listWidget: DownloadWidgetList):
        self._downloadWidgetList = []
        self._downloaderList = []
        self._downloadConfig = config.getDownloadConfig()
        self._config = config
        self._listWidget = listWidget

    def readPausedDownload(self):
        download_info_path = Path(self._downloadConfig['downloadInfoPath'])
        if not download_info_path.exists():
            return

        for file in download_info_path.iterdir():
            if file.is_file() and file.suffix == ".json":
                download_info = Config.readJson(file)
                self.startDownload(download_info=download_info)

    def newDownload(self, url: str):
        if self.checkRepeatDownloader(url):
            return
        self.startDownload(url=url)

    def checkRepeatDownloader(self, url: str):
        for downloader in self._downloaderList:
            if downloader.fileInfo.url == url:
                return True
        return False

    def startDownload(self, url=None, download_info=None):
        downloader = self.buildDownloader()

        if url:
            downloader.mode = lambda: downloader.creatNewDownload(url)
        elif download_info:
            downloader.mode = lambda: downloader.creatPauseDownload(download_info)
        else:
            raise ValueError("Either url or download_info must be provided")

        downloader.start()
        self._downloaderList.append(downloader)

    def buildDownloader(self) -> Downloader:
        downloader = Downloader(self._config)

        widget = self.getWidgetWithDownloader(downloader)
        self._downloadWidgetList.append(widget)
        self._listWidget.addDownloadWidget(widget)

        return downloader

    @staticmethod
    def getWidgetWithDownloader(downloader: Downloader) -> DownloadWidget:
        widget = DownloadWidget()
        downloader.progress.updateProgress.connect(widget.updateProgress)
        downloader.speed.updateSpeed.connect(widget.updateDownloadSpeed)
        downloader.state.updateState.connect(widget.updateState)
        widget.initDownload(downloader)
        downloader.progress.updateProgress.connect(widget.moreInfo.updateProgress)
        downloader.speed.updateSpeed.connect(widget.moreInfo.updateSpeed)
        downloader.state.updateState.connect(widget.moreInfo.updateState)
        downloader.fileInfo.error.updateError.connect(widget.moreInfo.updateError)
        return widget

# def splitRange(self, start, end):
#     totalRange = end - start
#     splitSize = totalRange // self._maxThread
#     ranges = []
#     for i in range(self._maxThread):
#         splitStart = start + i * splitSize
#         splitEnd = splitStart + splitSize - 1
#         if i == self._maxThread - 1:
#             splitEnd = end
#         ranges.append([splitStart, splitStart, splitEnd])
#     return ranges
