# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'moreInfo.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QProgressBar,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(680, 364)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.bigProgress = QProgressBar(Form)
        self.bigProgress.setObjectName(u"bigProgress")
        self.bigProgress.setMaximum(100)
        self.bigProgress.setValue(0)
        self.bigProgress.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)
        self.bigProgress.setOrientation(Qt.Horizontal)
        self.bigProgress.setTextDirection(QProgressBar.BottomToTop)

        self.verticalLayout.addWidget(self.bigProgress)


        self.gridLayout_2.addLayout(self.verticalLayout, 2, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.fileNameLabel = QLabel(Form)
        self.fileNameLabel.setObjectName(u"fileNameLabel")

        self.gridLayout.addWidget(self.fileNameLabel, 0, 1, 1, 1)

        self.saveLabel = QLabel(Form)
        self.saveLabel.setObjectName(u"saveLabel")

        self.gridLayout.addWidget(self.saveLabel, 5, 1, 1, 1)

        self.fileSizeLabel = QLabel(Form)
        self.fileSizeLabel.setObjectName(u"fileSizeLabel")

        self.gridLayout.addWidget(self.fileSizeLabel, 2, 1, 1, 1)

        self.stateLabel = QLabel(Form)
        self.stateLabel.setObjectName(u"stateLabel")

        self.gridLayout.addWidget(self.stateLabel, 4, 1, 1, 1)

        self.label_1 = QLabel(Form)
        self.label_1.setObjectName(u"label_1")
        self.label_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.urlLabel = QLabel(Form)
        self.urlLabel.setObjectName(u"urlLabel")

        self.gridLayout.addWidget(self.urlLabel, 1, 1, 1, 1)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.speedLabel = QLabel(Form)
        self.speedLabel.setObjectName(u"speedLabel")

        self.gridLayout.addWidget(self.speedLabel, 3, 1, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)

        self.errorLabel = QLabel(Form)
        self.errorLabel.setObjectName(u"errorLabel")

        self.gridLayout.addWidget(self.errorLabel, 6, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 7, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.bigProgress.setFormat(QCoreApplication.translate("Form", u"%p%", None))
        self.fileNameLabel.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.saveLabel.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.fileSizeLabel.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.stateLabel.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_1.setText(QCoreApplication.translate("Form", u"File Name:", None))
        self.label.setText(QCoreApplication.translate("Form", u"Download Speed:", None))
        self.urlLabel.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Save To:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Url:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"File Size:", None))
        self.speedLabel.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"State:", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Error", None))
        self.errorLabel.setText(QCoreApplication.translate("Form", u"Null", None))
    # retranslateUi

