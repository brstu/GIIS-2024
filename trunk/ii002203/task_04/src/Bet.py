from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5 import QtGui


class BetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ставка")
        self.setGeometry(0, 0, 300, 50)

        x = parent.geometry().x() + int((parent.geometry().width() - self.geometry().width()) / 2)
        y = parent.geometry().y() + int((parent.geometry().height() - self.geometry().height()) / 2)
        self.move(x, y)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        self.labelInputBet = QLabel("Введите ставку:")
        self.labelInputBet.setFont(font)

        font.setPointSize(14)
        self.lineInputBet = QLineEdit()
        self.lineInputBet.setFont(font)

        self.buttonAccept = QPushButton("Принять")
        self.buttonAccept.setFont(font)

        layout = QVBoxLayout()
        layout.addWidget(self.labelInputBet)
        layout.addWidget(self.lineInputBet)
        layout.addWidget(self.buttonAccept)

        self.setLayout(layout)
