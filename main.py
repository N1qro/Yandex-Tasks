import random
import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtCore import QPoint, QRect, QSize, Qt, QVariant, pyqtSignal
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QLabel,
                             QTableWidgetItem, QVBoxLayout, QWidget)

from os.path import join
from UI.addEditCoffeeForm_UI import Ui_Form as editUI
from UI.main_UI import Ui_Form as mainUI

class EntryEditWindow(QWidget, editUI):
    entryChanged = pyqtSignal()

    def __init__(self, *args, mode='edit', maxId=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.mode = mode
        self.closeButton.clicked.connect(self.close)
        self.submitButton.clicked.connect(self.onSubmit)
        self.idBox.valueChanged.connect(self.onIdChange)
        self.idBox.setMaximum(maxId)
        self.loadCheckboxes()

        if mode == 'add':
            self.setWindowTitle('Добавление новой записи')
            self.label.setText('Добавление нового вида кофе')
            self.idBox.hide()
            self.text7.hide()
        else:
            self.onIdChange(1)

    def onIdChange(self, entryId):
        db = sqlite3.connect(join('data', 'coffee.db'))
        cursor = db.cursor()

        _, grade, degree, coffeeType, desc, price, volume = cursor.execute(
            f"SELECT * FROM info WHERE id = {entryId}").fetchone()
        self.gradeBox.setCurrentText(grade)
        self.degreeBox.setCurrentText(degree)
        self.typeBox.setCurrentText(coffeeType)
        self.descriptionBox.setText(desc)
        self.priceBox.setValue(price)
        self.volumeBox.setValue(volume)

    def loadCheckboxes(self):
        db = sqlite3.connect(join('data', 'coffee.db'))
        grades = db.cursor().execute('SELECT grade FROM grades').fetchall()
        degrees = db.cursor().execute('SELECT degree FROM degrees').fetchall()
        types = db.cursor().execute('SELECT type FROM types').fetchall()
        db.close()

        self.gradeBox.addItems(grade[0] for grade in grades)
        self.degreeBox.addItems(degree[0] for degree in degrees)
        self.typeBox.addItems(_type[0] for _type in types)

    def onSubmit(self):
        entryId = self.idBox.value()
        grade = self.gradeBox.currentText()
        degree = self.degreeBox.currentText()
        coffeeType = self.typeBox.currentText()
        description = self.descriptionBox.toPlainText()
        price = self.priceBox.value()
        volume = self.volumeBox.value()

        queryData = [grade, degree, coffeeType, description, price, volume]
        if self.mode == 'add':
            query = """
                INSERT INTO info (grade, degree, type, description, price, volume)
                VALUES (?,?,?,?,?,?)
            """
        else:
            query = """
                UPDATE info SET grade = ?, degree = ?, type = ?, description = ?, price = ?, volume = ? WHERE id = ?
            """
            queryData.append(entryId)

        db = sqlite3.connect(join('data', 'coffee.db'))
        cursor = db.cursor()
        cursor.execute(query, queryData)
        db.commit()
        db.close()
        self.entryChanged.emit()
        self.close()


class CustomDialog(QDialog):
    def __init__(self, *args, title='Confirmation window', msg='', **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(title)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class Window(QWidget, mainUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.clearButton.clicked.connect(self.onClear)
        self.refreshButton.clicked.connect(self.onRefresh)
        self.addButton.clicked.connect(self.onAdd)
        self.editButton.clicked.connect(self.onEdit)
        self.lastFetchedData = list()
        self.onRefresh()

    def onAdd(self):
        self.onRefresh()
        self.newEntryWindow = EntryEditWindow(
            mode='add', maxId=self.tableWidget.rowCount())
        self.newEntryWindow.show()
        self.newEntryWindow.entryChanged.connect(self.onRefresh)

    def onEdit(self):
        self.onRefresh()
        self.newEntryWindow = EntryEditWindow(
            mode='edit', maxId=self.tableWidget.rowCount())
        self.newEntryWindow.show()
        self.newEntryWindow.entryChanged.connect(self.onRefresh)

    def onClear(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.clear()

    def onRefresh(self, *a):
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

            self.lastFetchedData.append(data)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.adjustSize()

    def getDBInfo(self):
        db = sqlite3.connect(join('data', 'coffee.db'))
        cursor = db.cursor()
        return cursor.execute('SELECT * FROM info').fetchall()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
