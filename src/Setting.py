import re
from pathlib import Path
from typing import List, Dict, Tuple, Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QPushButton, QLayout, QLabel, \
    QHBoxLayout, \
    QSpinBox, QFontComboBox, QSizePolicy, QSpacerItem, QCheckBox, QVBoxLayout, \
    QGridLayout, QFileDialog, QScrollArea
from qfluentwidgets import ComboBox, LineEdit, ColorDialog
from config import Config

SETTING_VALUE_TYPE = str | List | Dict | int | bool


class SettingTextCompiler:
    def __init__(self):
        self.dropDownPattern = r'^([^?]+) \? ([^|]+) \| ([^|]+)$'
        self.colorEditPattern = r'^[a-z]+-[a-z]+-color$'

    def isDropDownBox(self, s: str) -> bool:
        return re.match(self.dropDownPattern, s) is not None

    def isColorEdit(self, s: str) -> bool:
        return re.match(self.colorEditPattern, s) is not None

    def getDropDownValue(self, value: str) -> Tuple[str | None, List[str] | None]:
        match = re.match(self.dropDownPattern, value)
        if match:
            val = match.group(1)
            options = [match.group(2), match.group(3)]
            return val, options
        return None, None

    def modifyDropDownValue(self, oldVal: str, newVal: str) -> str | None:
        match = re.match(self.dropDownPattern, oldVal)
        if match:
            options = [match.group(2), match.group(3)]
            return f"{newVal} ? {options[0]} | {options[1]}"
        return None

    def getValueType(self, key: str, value: SETTING_VALUE_TYPE):
        if isinstance(value, str):
            typeVal = "str"
            if Path(value).is_dir():
                typeVal = "path"
            elif self.isDropDownBox(value):
                typeVal = 'dropDown'
            elif self.isColorEdit(key):
                typeVal = 'color'
        else:
            typeVal = value.__class__.__name__

        return typeVal


class SettingComponent:

    def __init__(self, valueChange: Callable, listValueChange: Callable, settingWindow: QWidget):
        self._defaultValue = None
        self._displayText = None
        self._name = None
        self.compiler = None

        self._valueChange = valueChange
        self._listValueChange = listValueChange

        self.translate_ = settingWindow.tr
        self.window = settingWindow

        self.typeCompareDict = {
            'int': self.addNumberInput,
            'dict': self.addDictInput,
            'list': self.addListInput,
            'str': self.addStrInput,
            "path": self.addPathInput,
            'dropDown': self.addDropDownInput,
            'color': self.addColorInput
        }

    def buildWidget(self, name: str, displayText: str, defaultValue: SETTING_VALUE_TYPE) -> QWidget | None:
        self._name = name
        self._displayText = displayText + ":"
        self._defaultValue: SETTING_VALUE_TYPE = defaultValue
        self.compiler = SettingTextCompiler()

        widget = QWidget()

        valueType = self.compiler.getValueType(name, self._defaultValue)

        layout = self.typeCompareDict.get(valueType)

        if layout:
            layout = layout()
            widget.setLayout(layout)
            return widget
        else:
            return None

    def addColorInput(self) -> QLayout:
        layout = QHBoxLayout()
        label = QLabel()
        label.setText(self._displayText)

        layout.addWidget(label)

        lineEdit = LineEdit()
        lineEdit.setObjectName(self._name)
        lineEdit.setText(self._defaultValue)

        layout.addWidget(lineEdit)
        colorSelectBtn = QPushButton()
        colorSelectBtn.setIcon(QIcon(':/setting/palette.svg'))
        colorSelectBtn.setObjectName("colorSelectBtn")
        colorDialog = ColorDialog(self._defaultValue, title=f'{self.translate_("Select color for")} {self._displayText}', parent=self.window)
        colorDialog.close()
        colorSelectBtn.clicked.connect(lambda: colorDialog.show())
        colorDialog.colorChanged.connect(lambda color: lineEdit.setText(color.name()))
        layout.addWidget(colorSelectBtn)
        lineEdit.textChanged.connect(lambda text: self._valueChange(lineEdit.objectName(), text))

        return layout

    def addDropDownInput(self) -> QLayout:
        layout = QHBoxLayout()
        label = QLabel()
        label.setText(self._displayText)

        layout.addWidget(label)

        value, valueList = self.compiler.getDropDownValue(self._defaultValue)

        comboBox = ComboBox()
        comboBox.setObjectName(self._name)
        comboBox.setToolTip(self._defaultValue)
        comboBox.addItems(valueList)
        comboBox.setCurrentText(value)

        layout.addWidget(comboBox)

        def changeDropDownValue(newVal):
            newVal = self.compiler.modifyDropDownValue(comboBox.toolTip(), newVal)
            if newVal:
                self._valueChange(comboBox.objectName(), newVal)

        comboBox.currentTextChanged.connect(changeDropDownValue)

        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addItem(horizontalSpacer)
        return layout

    def addDictInput(self) -> QLayout:
        gridLayout = QGridLayout()
        label = QLabel()
        label.setText(self._displayText)
        gridLayout.addWidget(label, 0, 0, 1, 1)

        widget = QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(sizePolicy)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        for key, val in self._defaultValue.items():
            widgetComponent = self.buildWidget(key, self.translate_(key), val)
            layout.addWidget(widgetComponent)
        widget.setLayout(layout)
        gridLayout.addWidget(widget, 1, 0, 1, 1)

        return gridLayout

    def addListInput(self) -> QLayout:
        layout = QVBoxLayout()
        label = QLabel()
        label.setText(self._displayText)
        layout.addWidget(label)
        text = LineEdit()
        displayText = " ".join(self._defaultValue)
        text.setText(displayText)
        text.setObjectName(self._name)
        text.textChanged.connect(lambda: self._listValueChange(text.objectName(), text.text()))
        layout.addWidget(text)
        return layout

    def addNumberInput(self) -> QLayout:
        layout = QHBoxLayout()

        label = QLabel()
        label.setText(self._displayText)

        layout.addWidget(label)

        spinBox = QSpinBox()
        spinBox.setObjectName(self._name)
        spinBox.setValue(self._defaultValue)
        spinBox.valueChanged.connect(lambda value: self._valueChange(spinBox.objectName(), value))

        layout.addWidget(spinBox)

        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        layout.addItem(horizontalSpacer)

        return layout

    def addRadioInput(self) -> QLayout:
        layout = QHBoxLayout()

        checkBox = QCheckBox()
        checkBox.setObjectName(self._name)
        checkBox.setText(self._displayText)
        checkBox.setChecked(self._defaultValue)

        layout.addWidget(checkBox)

        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        layout.addItem(horizontalSpacer)

        checkBox.stateChanged.connect(lambda state: self._valueChange(checkBox.objectName(), state))

        return layout

    def addStrInput(self) -> QLayout:
        layout = QHBoxLayout()
        label = QLabel()
        label.setText(self._displayText)

        layout.addWidget(label)

        lineEdit = LineEdit()
        lineEdit.setObjectName(self._name)
        lineEdit.setText(self._defaultValue)

        layout.addWidget(lineEdit)

        lineEdit.textChanged.connect(lambda text: self._valueChange(lineEdit.objectName(), text))

        return layout

    def addFontInput(self) -> QLayout:
        layout = QHBoxLayout()
        label = QLabel()
        label.setText(self._displayText)

        layout.addWidget(label)

        fontComboBox = QFontComboBox()
        fontComboBox.setDisplayFont(self._defaultValue, self._defaultValue)
        fontComboBox.setObjectName(self._name)

        layout.addWidget(fontComboBox)

        fontComboBox.currentFontChanged.connect(lambda font: self._valueChange(fontComboBox.objectName(), font))

        return layout

    def addPathInput(self) -> QLayout:
        layout = QHBoxLayout()
        label = QLabel()
        label.setText(self._displayText)

        layout.addWidget(label)

        lineEdit = LineEdit()
        lineEdit.setObjectName(self._name)
        lineEdit.setText(self._defaultValue)

        layout.addWidget(lineEdit)

        lineEdit.textChanged.connect(lambda text: self._valueChange(lineEdit.objectName(), text))

        pushButton = QPushButton()
        pushButton.setIcon(QIcon(':/setting/file.svg'))
        fileDialog = QFileDialog(self.window)
        fileDialog.setWindowTitle(f'{self.translate_("Select directory for")} {self._displayText}')
        fileDialog.setStyleSheet("color: black;")
        fileDialog.setFileMode(QFileDialog.FileMode.Directory)
        fileDialog.setDirectory(self._defaultValue)
        fileDialog.accepted.connect(lambda: lineEdit.setText(fileDialog.directory().absolutePath()))
        pushButton.clicked.connect(fileDialog.show)
        pushButton.setObjectName("fileSelectBtn")

        layout.addWidget(pushButton)

        return layout


class Setting:
    def __init__(self, config: Config, window: QWidget):
        super().__init__()

        self.window = window
        self.translate = window.tr
        self.config = config
        self.configTran = config.getConfigTran()

        self.settingCom = SettingComponent(self.valueChange, self.listValueChange, window)
        self.page = QWidget()
        self.page.setObjectName('page')
        self.grid = QGridLayout()
        self.scrollArea = QScrollArea()
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName('scrollAreaWidgetContents')
        self.scrollArea.setObjectName('scrollArea')
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.pageLayout = QVBoxLayout()

    def buildSettingPage(self):
        for titleName in self.config.config.keys():
            titleWidget = QWidget()
            titleLayout = QVBoxLayout()
            titleWidget.setLayout(titleLayout)
            titleWidget.setObjectName('titleWidget')

            titleLabel = QLabel()
            titleLabel.setText(self.translate(titleName))
            titleLabel.setObjectName('titleLabel')
            titleLayout.addWidget(titleLabel)

            for name, val in self.config.config[titleName].items():
                displayText = self.translate(name)
                widget = self.settingCom.buildWidget(name, displayText, val)
                if widget:
                    titleLayout.addWidget(widget)

            titleWidget.setLayout(titleLayout)
            self.pageLayout.addWidget(titleWidget)

            horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.pageLayout.addItem(horizontalSpacer)

        self.scrollAreaWidgetContents.setLayout(self.pageLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.grid.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.page.setLayout(self.grid)

    def updateConfig(self, d: Dict, name, new_value):
        for key, value in d.items():
            if isinstance(value, dict):
                self.updateConfig(value, name, new_value)
            if key == name:
                d[key] = new_value
        return d

    def valueChange(self, name: str, newValue):
        self.config.config = self.updateConfig(self.config.config, name, newValue)
        self.config.save()

    def listValueChange(self, name: str, newValue: str):
        self.valueChange(name, newValue.split(' '))
