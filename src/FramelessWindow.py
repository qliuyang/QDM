from PySide6.QtGui import QColor, QCursor
from PySide6.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QWidget
import enum
from PySide6.QtCore import Qt, QRect


class CursorDirection(enum.Enum):
    default = -1
    up = 0
    down = 1
    left = 2
    right = 3
    leftTop = 4
    leftBottom = 5
    rightBottom = 6
    rightTop = 7


class FramelessWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dragPoint = None
        self.leftBtnPressed = None
        self.cursorDirection = None

    def setupUi(self, parent):
        def moveTitlebar(_event):
            self.windowHandle().startSystemMove()

        shadow = QGraphicsDropShadowEffect()  # 设定一个阴影,半径为 4,颜色为 2, 10, 25,偏移为 0,0
        shadow.setBlurRadius(4)
        shadow.setColor(QColor(2, 10, 25))
        shadow.setOffset(0, 0)

        parent.ui.mainWidget.setGraphicsEffect(shadow)

        parent.ui.headBar.mouseMoveEvent = moveTitlebar

        parent.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        parent.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def getCursorDirection(self, globalPoint):
        padding = 3

        rect = self.rect()
        topLeft = self.mapToGlobal(rect.topLeft())
        bottomRight = self.mapToGlobal(rect.bottomRight())

        x = globalPoint.x()
        y = globalPoint.y()

        if topLeft.x() + padding >= x >= topLeft.x() and topLeft.y() + padding >= y >= topLeft.y():
            self.cursorDirection = CursorDirection.leftTop
            self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        elif bottomRight.x() - padding <= x <= bottomRight.x() and bottomRight.y() - padding <= y <= bottomRight.y():
            self.cursorDirection = CursorDirection.rightBottom
            self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
        elif topLeft.x() + padding >= x >= topLeft.x() and bottomRight.y() - padding <= y <= bottomRight.y():
            self.cursorDirection = CursorDirection.leftBottom
            self.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        elif bottomRight.x() >= x >= bottomRight.x() - padding and topLeft.y() <= y <= topLeft.y() + padding:
            self.cursorDirection = CursorDirection.rightTop
            self.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        elif topLeft.x() + padding >= x >= topLeft.x():
            self.cursorDirection = CursorDirection.left
            self.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        elif bottomRight.x() >= x >= bottomRight.x() - padding:
            self.cursorDirection = CursorDirection.right
            self.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        elif topLeft.y() <= y <= topLeft.y() + padding:
            self.cursorDirection = CursorDirection.up
            self.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        elif bottomRight.y() >= y >= bottomRight.y() - padding:
            self.cursorDirection = CursorDirection.down
            self.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        else:
            self.cursorDirection = CursorDirection.default
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftBtnPressed = True

            if self.cursorDirection != CursorDirection.default:
                self.mouseGrabber()
            else:
                self.dragPoint = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        globalPoint = event.globalPosition().toPoint()
        rect = self.rect()
        topLeft = self.mapToGlobal(rect.topLeft())
        bottomRight = self.mapToGlobal(rect.bottomRight())

        if not self.leftBtnPressed:
            self.getCursorDirection(globalPoint)
        else:
            if self.cursorDirection != CursorDirection.default:
                moveRect = QRect(topLeft, bottomRight)

                if self.cursorDirection == CursorDirection.left:
                    if bottomRight.x() - globalPoint.x() <= self.minimumWidth():
                        moveRect.setX(topLeft.x())
                    else:
                        moveRect.setX(globalPoint.x())
                elif self.cursorDirection == CursorDirection.right:
                    moveRect.setWidth(globalPoint.x() - topLeft.x())
                elif self.cursorDirection == CursorDirection.up:
                    if bottomRight.y() - globalPoint.y() <= self.minimumHeight():
                        moveRect.setY(topLeft.y())
                    else:
                        moveRect.setY(globalPoint.y())
                elif self.cursorDirection == CursorDirection.down:
                    moveRect.setHeight(globalPoint.y() - topLeft.y())
                elif self.cursorDirection == CursorDirection.leftTop:
                    if bottomRight.x() - globalPoint.x() <= self.minimumWidth():
                        moveRect.setX(topLeft.x())
                    else:
                        moveRect.setX(globalPoint.x())

                    if bottomRight.y() - globalPoint.y() <= self.minimumHeight():
                        moveRect.setY(topLeft.y())
                    else:
                        moveRect.setY(globalPoint.y())
                elif self.cursorDirection == CursorDirection.rightTop:
                    moveRect.setWidth(globalPoint.x() - topLeft.x())
                    moveRect.setY(globalPoint.y())
                elif self.cursorDirection == CursorDirection.leftBottom:
                    moveRect.setX(globalPoint.x())
                    moveRect.setHeight(globalPoint.y() - topLeft.y())
                elif self.cursorDirection == CursorDirection.rightBottom:
                    moveRect.setWidth(globalPoint.x() - topLeft.x())
                    moveRect.setHeight(globalPoint.y() - topLeft.y())
                else:
                    pass

                self.setGeometry(moveRect)
            else:
                self.move(event.globalPosition().toPoint() - self.dragPoint)
                event.accept()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.leftBtnPressed = False

            if self.cursorDirection != CursorDirection.default:
                self.releaseMouse()
                self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
