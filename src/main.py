import sys

from PySide6.QtCore import QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QPushButton
from qfluentwidgets import setTheme, Theme
from qframelesswindow import FramelessMainWindow

from DownloadEngine import DownloadEngine
from Setting import Setting, SettingTextCompiler
from Ui_MainWindow import Ui_MainWindow
from config import Config, Style
import main_rc


class MainWindow(FramelessMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.enableStyle = None
        self.configTran = None
        self.state = None
        self.translator = None

        self.downloadWidgetList = []
        self.downloaderList = []

        # 读取配置文件
        self.config = Config()
        self.windowConfig = self.config.getWindowConfig()
        self.downloadConfig = self.config.getDownloadConfig()
        self.styleObj = self.getWindowStyle()

        # 设置
        self.setWindowSetting()
        self.setWindowStyle()

        # 创建主界面
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 创建设置界面
        self.setting = Setting(self.config, self)
        self.initSettingPage()

        self.initUi()

        # 创建下载引擎 + 读取历史下载
        self.downloadEngine = DownloadEngine(self.config, self.ui.downloadList)
        self.downloadEngine.readPausedDownload()

        # 主界面连接信号槽
        self.ui.settingPageBtn.clicked.connect(lambda: self.changeMainStackPage(self.ui.settingPageBtn))
        self.ui.downloadPageBtn.clicked.connect(lambda: self.changeMainStackPage(self.ui.downloadPageBtn))
        self.ui.downloadListPageBtn.clicked.connect(lambda: self.changeMainStackPage(self.ui.downloadListPageBtn))
        self.ui.searchLineEdit.textChanged.connect(self.search)
        self.ui.newDownloadEdit.returned.connect(self.downloadEngine.newDownload)

        self.titleBar.raise_()

    def flushText(self):
        self.state = {
            "DOWNLOADING_STATE": self.tr("Downloading"),
            "PAUSE_STATE": self.tr("Pause"),
            "COMPLETED_STATE": self.tr("Completed"),
            "ERROR_STATE": self.tr("Error"),
            "READY_STATE": self.tr("Ready"),
            "WAITING_STATE": self.tr("Waiting"),
        }
        self.configTran = [
            self.tr('window'),
            self.tr('fileType'),
            self.tr('proxy'),
            self.tr("download"),
            self.tr("theme"),
            self.tr("language"),
            self.tr("tempPath"),
            self.tr("downloadInfoPath"),
            self.tr("output"),
            self.tr("compressed"),
            self.tr("application"),
            self.tr("video"),
            self.tr("document"),
            self.tr("http"),
            self.tr("https"),
            self.tr('select color with {self._name}'),
            self.tr('select path with {self._name}'),
            self.tr('light-bar-color'),
            self.tr('light-basic-color'),
            self.tr('light-font-color'),
            self.tr('dark-basic-color'),
            self.tr('dark-font-color'),
            self.tr('dark-bar-color'),
        ]

        self.config.setStateConfig(self.state)
        self.config.setConfigTran(self.configTran)

    def changeMainStackPage(self, btn: QPushButton):
        # 映射按钮和对应的页面索引
        btnIndexMap = {
            self.ui.downloadListPageBtn: 0,
            self.ui.settingPageBtn: 2,
            self.ui.downloadPageBtn: 1
        }

        for button, index in btnIndexMap.items():
            if button == btn:
                self.ui.mainStack.setCurrentIndex(index)  # 切换页面
                button.setStyleSheet(self.enableStyle)  # 设置选中样式
            else:
                button.setStyleSheet('')

    def initSettingPage(self):
        self.setting.buildSettingPage()
        self.ui.mainStack.addWidget(self.setting.page)

    def setWindowStyle(self):
        self.setStyleSheet(self.styleObj.style)

        if self.styleObj.styleTheme == "light":
            setTheme(Theme.LIGHT)
        elif self.styleObj.styleTheme == "dark":
            setTheme(Theme.DARK)

        self.enableStyle = self.styleObj.getClickedStyle()

    def setButtonIcons(self):
        """
        设置按钮图标
        """
        theme = self.styleObj.styleTheme
        icons = {
            "settingPageBtn": f":/{theme}/setting-{theme}.svg",
            "downloadPageBtn": f":/{theme}/download-{theme}.svg",
            "downloadListPageBtn": f":/{theme}/downloadList-{theme}.svg"
        }
        for btn_name, icon_path in icons.items():
            getattr(self.ui, btn_name).setIcon(QIcon(icon_path))

    def initUi(self):
        self.ui.downloadPageBtn.setStyleSheet(self.enableStyle)
        self.setWindowIcon(QIcon(":/toolBar/QDM.png"))
        self.setButtonIcons()

    def getWindowStyle(self) -> Style:
        style = self.windowConfig.get("theme")
        style = SettingTextCompiler().getDropDownValue(style)[0]

        styleObj = Style(self.__class__.__name__, style, self.config)
        styleObj.buildStyle()

        return styleObj

    def setWindowSetting(self):
        language = self.windowConfig.get("language")
        language = SettingTextCompiler().getDropDownValue(language)[0]

        self.translator = QTranslator()
        self.translator.load(f"qm/main.qm")

        if language == "Chinese":
            if not self.translator.isEmpty():
                app.installTranslator(self.translator)
        elif language == "English":
            app.removeTranslator(self.translator)

        self.flushText()

    def search(self, text):
        self.ui.downloadList.filterItems(text)


def main():
    global app, window

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
