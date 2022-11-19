import random
import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QRect, QSize, QPoint
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import uic

MIN_RADIUS = 40
MAX_RADIUS = 60
COLORS = [  # Yellow color variants
    QColor(255, 211, 13),
    QColor(206, 161, 13),
    QColor(206, 123, 13),
    QColor(206, 87, 13),
    QColor(206, 87, 56)
]


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.toDraw = False
        self.circles = list()
        uic.loadUi('UI.ui', self)
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

        Color = random.choice(COLORS)
        self.circles.append((Circle, Color))
        self.paint()

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
