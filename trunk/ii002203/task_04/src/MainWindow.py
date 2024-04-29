import secrets

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import Qt
from Bet import BetDialog
from functools import partial
import time

red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

color_white_and_border  = "color: rgb(255, 255, 255);\nborder: 1px solid #FFFFFF;\n"
color_white = "color: rgb(255, 255, 255);\n"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.buttonStartAgain = None
        self.timer = QTimer()

        self.happyNumbers = None

        self.buttons = []

        self.labelResultNumber = None
        self.labelWinLoss = None
        self.labelBalance = None

        self.balance = 1000
        self.bet = 0
        self.multiplier = 0
        self.casinoNumber = 0

        self.initUI()
        self.betDialog = BetDialog(self)

        self.timer.timeout.connect(self.hideLabels)
        self.betDialog.buttonAccept.clicked.connect(self.getBet)

        self.centralWidget = None

    def initUI(self):
        self.setWindowTitle("Рулетка")
        self.setWindowIcon(QIcon("casino_icon.png"))
        self.setGeometry(400, 150, 1040, 600)
        self.setStyleSheet("background-color: rgb(0, 115, 0);")
        self.centralWidget = QtWidgets.QWidget()

        button_positions = [
            (140, 150), (140, 100), (140, 50),
            (200, 150), (200, 100), (200, 50),
            (260, 150), (260, 100), (260, 50),
            (320, 150), (320, 100), (320, 50),
            (380, 150), (380, 100), (380, 50),
            (440, 150), (440, 100), (440, 50),
            (500, 150), (500, 100), (500, 50),
            (560, 150), (560, 100), (560, 50),
            (620, 150), (620, 100), (620, 50),
            (680, 150), (680, 100), (680, 50),
            (740, 150), (740, 100), (740, 50),
            (800, 150), (800, 100), (800, 50)
        ]

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        i = 1
        while i <= 36:
            button = QtWidgets.QPushButton(str(i), self.centralWidget)
            button.setGeometry(button_positions[i - 1][0], button_positions[i - 1][1], 60, 50)
            button.setFont(font)

            if i in red:
                button.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border: 1px solid #FFFFFF;\n")
            elif i in black:
                button.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "border: 1px solid #FFFFFF;\n")

            button.clicked.connect(partial(self.onButtonAction, i))
            self.buttons.append(button)
            i += 1
        font.setFamily("Calibri")
        font.setPointSize(24)

        self.button0 = QtWidgets.QPushButton("0", self.centralWidget)
        self.button0.setGeometry(80, 50, 60, 150)
        self.button0.setFont(font)
        self.button0.setStyleSheet("background-color: #00DD00;\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border: 1px solid #FFFFFF;\n")
        i = 0
        self.button0.clicked.connect(partial(self.onButtonAction, i))
        self.buttons.append(self.button0)
        font.setFamily("Calibri")
        font.setPointSize(26)

        button_positions = [(140, 200), (380, 200), (620, 200)]

        button_names = [
            "1 to 12", "13 to 24", "25 to 36"
        ]

        temp = len(self.buttons)
        for i, position in enumerate(button_positions):
            button = QtWidgets.QPushButton(button_names[i], self.centralWidget)
            button.setGeometry(position[0], position[1], 240, 60)
            button.setFont(font)
            button.setStyleSheet(color_white_and_border)

            button.clicked.connect(partial(self.onButtonAction, i + temp))
            self.buttons.append(button)
        font.setFamily("Calibri")
        font.setPointSize(18)

        button_positions = [(860, 50), (860, 100), (860, 150)]

        temp = len(self.buttons)
        for i, position in enumerate(button_positions):
            button = QtWidgets.QPushButton("2 to 1", self.centralWidget)
            button.setGeometry(position[0], position[1], 100, 50)
            button.setFont(font)
            button.setStyleSheet(color_white_and_border)
            button.clicked.connect(partial(self.onButtonAction, (i + temp)))
            self.buttons.append(button)
        button_positions = [(140, 260), (260, 260), (620, 260), (740, 260)]

        button_names = (["1 to 18", "ЧЁТНОЕ", "НЕЧЁТНОЕ", "19 to 36"])
        temp = len(self.buttons)
        font.setPointSize(16)
        for i, position in enumerate(button_positions):
            button = QtWidgets.QPushButton(button_names[i], self.centralWidget)
            button.setGeometry(position[0], position[1], 120, 60)
            button.setFont(font)
            button.setStyleSheet(color_white_and_border)
            button.clicked.connect(partial(self.onButtonAction, (i + temp)))
            self.buttons.append(button)

        button_red = QtWidgets.QPushButton(self.centralWidget)
        button_red.setGeometry(380, 260, 120, 60)
        button_red.setFont(font)
        button_red.setStyleSheet("color: rgb(255, 255, 255);\n"
                                "border: 1px solid #FFFFFF;\n"
                                "background-color: rgb(255, 0, 0);\n")
        button_red.clicked.connect(partial(self.onButtonAction, 47))
        self.buttons.append(button_red)

        button_black = QtWidgets.QPushButton(self.centralWidget)
        button_black.setGeometry(500, 260, 120, 60)
        button_black.setFont(font)
        button_black.setStyleSheet("color: rgb(255, 255, 255);\n"
                                  "border: 1px solid #FFFFFF;\n"
                                  "background-color: rgb(0, 0, 0);\n")
        button_black.clicked.connect(partial(self.onButtonAction, 48))
        self.buttons.append(button_black)

        font.setPointSize(26)
        font.setBold(True)
        self.labelBalance = QtWidgets.QLabel(f"Баланс: {self.balance} руб.", self.centralWidget)
        self.labelBalance.setGeometry(20, 360, 400, 40)
        self.labelBalance.setFont(font)
        self.labelBalance.setStyleSheet(color_white)

        font.setPointSize(28)
        self.labelWinLoss = QtWidgets.QLabel(self.centralWidget)
        self.labelWinLoss.setGeometry(700, 360, 320, 160)
        self.labelWinLoss.setFont(font)
        self.labelWinLoss.setStyleSheet(color_white)

        font.setPointSize(20)
        self.buttonStartAgain = QtWidgets.QPushButton("Заново", self.centralWidget)
        self.buttonStartAgain.setGeometry(20, 500, 120, 60)
        self.buttonStartAgain.setFont(font)
        self.buttonStartAgain.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "background-color: gray;\n")

        font.setPointSize(72)
        font.setBold(True)
        self.labelResultNumber = QtWidgets.QLabel(self.centralWidget)
        self.labelResultNumber.setGeometry(420, 370, 200, 200)
        self.labelResultNumber.setFont(font)
        self.labelResultNumber.setAlignment(Qt.AlignCenter)
        self.labelResultNumber.setStyleSheet(color_white)

        self.buttonStartAgain.clicked.connect(self.onButtonStartAgain)

        self.setCentralWidget(self.centralWidget)

    def onButtonStartAgain(self):
        self.balance = 1000
        self.labelBalance.setText(f"Баланс: {self.balance} руб.")

    def onButtonAction(self, num):
        self.labelWinLoss.clear()
        self.labelResultNumber.clear()
        actions = {
            1: self.onButton1Action, 2: self.onButton2Action, 3: self.onButton3Action,
            4: self.onButton4Action, 5: self.onButton5Action, 6: self.onButton6Action,
            7: self.onButton7Action, 8: self.onButton8Action, 9: self.onButton9Action,
            10: self.onButton10Action, 11: self.onButton11Action, 12: self.onButton12Action,
            13: self.onButton13Action, 14: self.onButton14Action, 15: self.onButton15Action,
            16: self.onButton16Action, 17: self.onButton17Action, 18: self.onButton18Action,
            19: self.onButton19Action, 20: self.onButton20Action, 21: self.onButton21Action,
            22: self.onButton22Action, 23: self.onButton23Action, 24: self.onButton24Action,
            25: self.onButton25Action, 26: self.onButton26Action, 27: self.onButton27Action,
            28: self.onButton28Action, 29: self.onButton29Action, 30: self.onButton30Action,
            31: self.onButton31Action, 32: self.onButton32Action, 33: self.onButton33Action,
            34: self.onButton34Action, 35: self.onButton35Action, 36: self.onButton36Action,
            0: self.onButton0Action,
            37: self.onButton1_12Action, 38: self.onButton13_24Action, 39: self.onButton25_36Action,
            40: self.onButton2to1_3Action, 41: self.onButton2to1_2Action, 42: self.onButton2to1_1Action,
            43: self.onButton1to18Action, 44: self.onButtonEvenAction, 45: self.onButtonOddAction,
            46: self.onButton19to36Action, 47: self.onButtonRedAction, 48: self.onButtonBlackAction
        }

        handler = actions.get(num)
        if handler and callable(handler):
            handler()
        else:
            print(f"Нет обработчика для кнопки {num}")

    def onButton1Action(self):
        self.happyNumbers = [1]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton2Action(self):
        self.happyNumbers = [2]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton3Action(self):
        self.happyNumbers = [3]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton4Action(self):
        self.happyNumbers = [4]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton5Action(self):
        self.happyNumbers = [5]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton6Action(self):
        self.happyNumbers = [6]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton7Action(self):
        self.happyNumbers = [7]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton8Action(self):
        self.happyNumbers = [8]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton9Action(self):
        self.happyNumbers = [9]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton10Action(self):
        self.happyNumbers = [10]
        self.betDialog.exec_()

    def onButton11Action(self):
        self.happyNumbers = [11]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton12Action(self):
        self.happyNumbers = [12]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton13Action(self):
        self.happyNumbers = [13]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton14Action(self):
        self.happyNumbers = [14]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton15Action(self):
        self.happyNumbers = [15]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton16Action(self):
        self.happyNumbers = [16]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton17Action(self):
        self.happyNumbers = [17]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton18Action(self):
        self.happyNumbers = [18]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton19Action(self):
        self.happyNumbers = [19]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton20Action(self):
        self.happyNumbers = [20]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton21Action(self):
        self.happyNumbers = [21]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton22Action(self):
        self.happyNumbers = [22]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton23Action(self):
        self.happyNumbers = [23]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton24Action(self):
        self.happyNumbers = [24]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton25Action(self):
        self.happyNumbers = [25]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton26Action(self):
        self.happyNumbers = [26]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton27Action(self):
        self.happyNumbers = [27]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton28Action(self):
        self.happyNumbers = [28]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton29Action(self):
        self.happyNumbers = [29]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton30Action(self):
        self.happyNumbers = [30]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton31Action(self):
        self.happyNumbers = [31]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton32Action(self):
        self.happyNumbers = [32]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton33Action(self):
        self.happyNumbers = [33]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton34Action(self):
        self.happyNumbers = [34]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton35Action(self):
        self.happyNumbers = [35]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton36Action(self):
        self.happyNumbers = [36]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton0Action(self):
        self.happyNumbers = [0]
        self.multiplier = 35
        self.betDialog.exec_()

    def onButton2to1_1Action(self):
        self.happyNumbers = [i for i in range(1, 37) if i % 3 == 1]
        self.multiplier = 3
        self.betDialog.exec_()

    def onButton2to1_2Action(self):
        self.happyNumbers = [i for i in range(1, 37) if i % 3 == 2]
        self.multiplier = 3
        self.betDialog.exec_()

    def onButton2to1_3Action(self):
        self.happyNumbers = [i for i in range(1, 37) if i % 3 == 0]
        self.multiplier = 3
        self.betDialog.exec_()

    def onButton1_12Action(self):
        self.happyNumbers = [i for i in range(1, 13)]
        self.multiplier = 3
        self.betDialog.exec_()

    def onButton13_24Action(self):
        self.happyNumbers = [i for i in range(13, 25)]
        self.multiplier = 3
        self.betDialog.exec_()

    def onButton25_36Action(self):
        self.happyNumbers = [i for i in range(25, 37)]
        self.multiplier = 3
        self.betDialog.exec_()

    def onButton1to18Action(self):
        self.happyNumbers = [i for i in range(1, 18)]
        self.multiplier = 2
        self.betDialog.exec_()

    def onButton19to36Action(self):
        self.happyNumbers = [i for i in range(19, 36)]
        self.multiplier = 2
        self.betDialog.exec_()

    def onButtonEvenAction(self):
        self.happyNumbers = [i for i in range(1, 37) if i % 2 == 0]
        self.multiplier = 2
        self.betDialog.exec_()

    def onButtonOddAction(self):
        self.happyNumbers = [i for i in range(1, 37) if i % 2 != 0]
        self.multiplier = 2
        self.betDialog.exec_()

    def onButtonRedAction(self):
        self.happyNumbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.multiplier = 2
        self.betDialog.exec_()

    def onButtonBlackAction(self):
        self.happyNumbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        self.multiplier = 2
        self.betDialog.exec_()

    def getBet(self):
        msg_box = QMessageBox(QMessageBox.Information, "WARNING", "Ставка превышает баланс!")
        if self.betDialog.lineInputBet.text().isdigit():
            if float(self.betDialog.lineInputBet.text()) <= self.balance:
                self.bet = int(self.betDialog.lineInputBet.text())
                self.balance -= self.bet
                self.labelBalance.setText(f"Баланс: {self.balance} руб.")
                self.betDialog.lineInputBet.clear()
                self.betDialog.close()

                QApplication.processEvents()

                self.processCasinoNumber()
            else:
                self.betDialog.lineInputBet.clear()
                msg_box.exec_()

        else:
            self.betDialog.lineInputBet.clear()

    def processCasinoNumber(self):
        if self.timer.isActive():
            self.timer.stop()

        self.getCasinoNumber()

        if self.casinoNumber in self.happyNumbers:
            result = self.bet * self.multiplier
            self.labelWinLoss.setStyleSheet("color: rgb(0, 255, 0);\n")
            self.labelWinLoss.setText(f"Выигрыш!\n{result} руб.")
            self.balance += result
            self.labelBalance.setText(f"Баланс: {self.balance} руб.")
        else:
            self.labelWinLoss.setStyleSheet("color: rgb(255, 40, 0);\n")
            self.labelWinLoss.setText("Проигрыш")

        self.timer.start(4000)

    def getCasinoNumber(self):
        for _ in range(40):
            i = secrets.randbelow(37)
            self.checkNumberOnColor(i)
            time.sleep(0.1)
            self.labelResultNumber.setText(f"{i}")
            QApplication.processEvents()

        self.casinoNumber = secrets.randbelow(37)
        self.checkNumberOnColor(self.casinoNumber)
        time.sleep(0.08)
        self.labelResultNumber.setText(f"{self.casinoNumber}")

    def checkNumberOnColor(self, num):
        if num in red:
            self.labelResultNumber.setStyleSheet("color: rgb(255, 0, 0);\n")
        elif num in black:
            self.labelResultNumber.setStyleSheet("color: rgb(0, 0, 0);\n")
        else:
            self.labelResultNumber.setStyleSheet("color: rgb(0, 255, 0);\n")

    def hideLabels(self):
        self.labelResultNumber.clear()
        self.labelWinLoss.clear()
