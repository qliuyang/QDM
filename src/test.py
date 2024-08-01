from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from qfluentwidgets import FolderListDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setFixedSize(400, 300)
        color = FolderListDialog(['.', 'q'], 'wwwww', content='111', parent=self)
        # color.close()


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
