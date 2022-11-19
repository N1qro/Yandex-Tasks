import random
import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QRect, QSize, QPoint
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import uic
from UI import Ui_Form

MIN_RADIUS = 40
MAX_RADIUS = 60


class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.toDraw = False
        self.circles = list()
        self.drawButton.clicked.connect(self.onClick)

    def onClick(self):
        geometry = self.rect()
        topRight = geometry.topRight()
        topLeft = geometry.topLeft()

        randX, randY = random.randint(
            topLeft.x(), topRight.x()), random.randint(topLeft.y(), topRight.x())
        radius = random.randint(MIN_RADIUS, MAX_RADIUS)

        Circle = QRect()
        Circle.setSize(QSize(radius, radius))
        Circle.moveCenter(QPoint(randX, randY))

        Color = self.getRandomColor()
        self.circles.append((Circle, Color))
        self.paint()

    def getRandomColor(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return QColor(r, g, b)

    def paintCircles(self, qp: QPainter):
        for circle, color in self.circles:
            qp.setBrush(color)
            qp.drawEllipse(circle)

    def paint(self):
        self.toDraw = True
        self.repaint()

    def paintEvent(self, event):
        if self.toDraw:
            qp = QPainter()
            qp.begin(self)
            self.paintCircles(qp)
            qp.end()
            self.toDraw = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
