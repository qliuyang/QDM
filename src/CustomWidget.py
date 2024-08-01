from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QPlainTextEdit


class CustomPlainTextEdit(QPlainTextEdit):
    returned = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.returned.emit(self.toPlainText())
        else:
            super().keyPressEvent(event)
