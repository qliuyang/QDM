# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

from CustomWidget import CustomPlainTextEdit
from DownloadEngine import DownloadWidgetList
import main_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 560)
        self.mainWidget = QWidget(MainWindow)
        self.mainWidget.setObjectName(u"mainWidget")
        self.gridLayout_2 = QGridLayout(self.mainWidget)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(4, 4, 6, 4)
        self.leftBar = QWidget(self.mainWidget)
        self.leftBar.setObjectName(u"leftBar")
        self.verticalLayout = QVBoxLayout(self.leftBar)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.downloadPageBtn = QPushButton(self.leftBar)
        self.downloadPageBtn.setObjectName(u"downloadPageBtn")
        self.downloadPageBtn.setMinimumSize(QSize(0, 57))
        self.downloadPageBtn.setIconSize(QSize(44, 22))
        self.downloadPageBtn.setAutoDefault(False)
        self.downloadPageBtn.setFlat(False)

        self.verticalLayout.addWidget(self.downloadPageBtn)

        self.downloadListPageBtn = QPushButton(self.leftBar)
        self.downloadListPageBtn.setObjectName(u"downloadListPageBtn")
        self.downloadListPageBtn.setMinimumSize(QSize(0, 57))
        self.downloadListPageBtn.setIconSize(QSize(47, 22))

        self.verticalLayout.addWidget(self.downloadListPageBtn)

        self.settingPageBtn = QPushButton(self.leftBar)
        self.settingPageBtn.setObjectName(u"settingPageBtn")
        self.settingPageBtn.setMinimumSize(QSize(0, 57))
        self.settingPageBtn.setIconSize(QSize(44, 22))

        self.verticalLayout.addWidget(self.settingPageBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_2.addWidget(self.leftBar, 1, 0, 2, 1)

        self.stateBar = QWidget(self.mainWidget)
        self.stateBar.setObjectName(u"stateBar")
        self.horizontalLayout_3 = QHBoxLayout(self.stateBar)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.messageLabel = QLabel(self.stateBar)
        self.messageLabel.setObjectName(u"messageLabel")

        self.horizontalLayout_3.addWidget(self.messageLabel)

        self.versionLabel = QLabel(self.stateBar)
        self.versionLabel.setObjectName(u"versionLabel")

        self.horizontalLayout_3.addWidget(self.versionLabel)


        self.gridLayout_2.addWidget(self.stateBar, 2, 1, 1, 1)

        self.mainStack = QStackedWidget(self.mainWidget)
        self.mainStack.setObjectName(u"mainStack")
        self.mainStack.setFrameShape(QFrame.NoFrame)
        self.downloadListPage = QWidget()
        self.downloadListPage.setObjectName(u"downloadListPage")
        self.gridLayout = QGridLayout(self.downloadListPage)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")

        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.searchWidget = QWidget(self.downloadListPage)
        self.searchWidget.setObjectName(u"searchWidget")
        self.searchWidget.setMinimumSize(QSize(0, 43))
        self.horizontalLayout = QHBoxLayout(self.searchWidget)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.searchWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u" margin-left: 6px;")
        icon = QIcon()
        icon.addFile(u":/toolBar/search.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.pushButton)

        self.searchLineEdit = QLineEdit(self.searchWidget)
        self.searchLineEdit.setObjectName(u"searchLineEdit")

        self.horizontalLayout.addWidget(self.searchLineEdit)


        self.verticalLayout_2.addWidget(self.searchWidget)

        self.downloadList = DownloadWidgetList(self.downloadListPage)
        self.downloadList.setObjectName(u"downloadList")

        self.verticalLayout_2.addWidget(self.downloadList)


        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)

        self.mainStack.addWidget(self.downloadListPage)
        self.downloadPage = QWidget()
        self.downloadPage.setObjectName(u"downloadPage")
        self.gridLayout_3 = QGridLayout(self.downloadPage)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.newDownloadEdit = CustomPlainTextEdit(self.downloadPage)
        self.newDownloadEdit.setObjectName(u"newDownloadEdit")

        self.gridLayout_3.addWidget(self.newDownloadEdit, 0, 0, 1, 1)

        self.mainStack.addWidget(self.downloadPage)

        self.gridLayout_2.addWidget(self.mainStack, 1, 1, 1, 1)

        self.headBar = QWidget(self.mainWidget)
        self.headBar.setObjectName(u"headBar")
        self.horizontalLayout_2 = QHBoxLayout(self.headBar)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.iconApp = QPushButton(self.headBar)
        self.iconApp.setObjectName(u"iconApp")
        self.iconApp.setMinimumSize(QSize(60, 60))
        icon1 = QIcon()
        icon1.addFile(u":/toolBar/QDM.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.iconApp.setIcon(icon1)
        self.iconApp.setIconSize(QSize(47, 48))

        self.horizontalLayout_2.addWidget(self.iconApp)

        self.label = QLabel(self.headBar)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.gridLayout_2.addWidget(self.headBar, 0, 0, 1, 2)

        MainWindow.setCentralWidget(self.mainWidget)

        self.retranslateUi(MainWindow)

        self.downloadPageBtn.setDefault(False)
        self.mainStack.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.downloadPageBtn.setText("")
        self.downloadListPageBtn.setText("")
        self.settingPageBtn.setText("")
        self.messageLabel.setText(QCoreApplication.translate("MainWindow", u"https://github.com/qliuyang", None))
        self.versionLabel.setText(QCoreApplication.translate("MainWindow", u"V1.0 Demo", None))
        self.pushButton.setText("")
        self.searchLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the history download file", None))
        self.newDownloadEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the URL to add a new download task", None))
        self.iconApp.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"QDM - Quick Download Manager", None))
    # retranslateUi

