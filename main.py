import random
import sys
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5.QtCore import QRect, QSize, QPoint, Qt, QVariant
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import uic


class Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.clearButton.clicked.connect(self.onClear)
        self.refreshButton.clicked.connect(self.onRefresh)

        self.onRefresh()

    def onClear(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.clear()

    def onRefresh(self):
        title = ['grade', 'degree', 'type', 'description', 'price', 'volume']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for _id, *data in self.getDBInfo():
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(data):
                item = QTableWidgetItem()
                item.setData(Qt.ItemDataRole.EditRole, QVariant(elem))
                self.tableWidget.setItem(
                    _id - 1, j, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.adjustSize()

    def getDBInfo(self):
        db = sqlite3.connect('coffee.db')
        cursor = db.cursor()

        query = """
            SELECT * FROM info
        """

        return cursor.execute(query).fetchall()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
