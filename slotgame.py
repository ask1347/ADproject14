#-*- coding: utf-8 -*-

# Import PyQt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit
from PyQt5.QtWidgets import QToolButton, QStatusBar

from slot import Slot
import random


class SlotGame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # Title label
        label = QLabel('Slot Game!')
        font = label.font()
        font.setPointSize(font.pointSize() + 10)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)

        #slot number
        self.outputs = []
        self.outputs.append(QLineEdit(self))
        self.outputs.append(QLineEdit(self))
        self.outputs.append(QLineEdit(self))
        for output in self.outputs:
            output.setReadOnly(True)

        outputLayout = QGridLayout()
        for i in range(1, 4):
            outputLayout.addWidget(self.outputs[i-1], 0, i, 1, 1)

        slotlabel = QLabel("slot")
        slotlabel.setAlignment(Qt.AlignRight)

        # User interactions
        self.betButton = QToolButton(self)
        self.betButton.setText('Bet')
        self.newGameButton = QToolButton(self)
        self.newGameButton.setText('New Game')
        self.currentMoneyLabel = QLabel("money: ")
        self.currentMoney = QLineEdit()
        self.currentMoney.setReadOnly(True)
        self.stakeLabel = QLabel("stake: ")
        self.stake = QLineEdit()
        self.count = QLineEdit("Left trials: ", self)
        self.count.setReadOnly(True)
        self.statusBar = QLineEdit("status", self)
        self.statusBar.setReadOnly(True)

        userLayout = QGridLayout()
        userLayout.addWidget(self.betButton, 0, 0)
        userLayout.addWidget(self.newGameButton, 1, 0)
        userLayout.addWidget(self.currentMoneyLabel, 0, 1)
        userLayout.addWidget(self.currentMoney, 0, 2)
        userLayout.addWidget(self.stakeLabel, 1, 1)
        userLayout.addWidget(self.stake, 1, 2)
        userLayout.addWidget(self.count, 2, 0)
        userLayout.addWidget(self.statusBar, 2, 1)

        # Layout
        mainLayout = QGridLayout()
        mainLayout.addWidget(label, 0, 0)
        mainLayout.addLayout(outputLayout, 1, 0)
        mainLayout.addLayout(userLayout, 2, 0)
        self.setLayout(mainLayout)

class mainWindow(QMainWindow):

    # Define the digit count used in the game

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize the main widget
        self.gameWidget = SlotGame()
        self.setCentralWidget(self.gameWidget)

        # Window title & status bar
        self.setWindowTitle('ADProject Slotmachine')
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)

        # Connect button callbacks
        self.gameWidget.betButton.clicked.connect(self.buttonClicked)
        self.gameWidget.newGameButton.clicked.connect(self.buttonClicked)

        self.currentMoney = 1000
        self.gameWidget.currentMoney.setText(str(self.currentMoney))

        #실행횟수를 5회로 제한
        self.currentTrial = 5
        self.gameWidget.count.setText("Left trials: " + str(self.currentTrial))

        # 게임이 시작될때 슬롯값을 비우는 기능
        self.game = Slot()
        self.slotValue = [None, None, None]

    def buttonClicked(self):
        button = self.sender()
        key = button.text()
        stake = 0

        if key == 'Bet':
            print("Betting")
            if self.currentTrial <= 0:
                print("no trial left")
                return
            self.currentTrial -= 1
            self.gameWidget.count.setText(str(self.currentTrial))
            try:
                stake = int(self.gameWidget.stake.text())
                self.currentMoney -= stake
                self.gameWidget.currentMoney.setText(str(self.currentMoney))
            except ValueError as e:
                print("there is no stake value")
                return
            
            self.gameWidget.stake.clear()

            self.slotValue = Slot.roll()
            for i in range(len(self.slotValue)):
                self.gameWidget.outputs[i].setText(str(self.slotValue[i]))
            if self.slotValue[0] == self.slotValue[1] and self.slotValue[0] == self.slotValue[2]:
                self.gameWidget.statusBar.setText("good job")
                print("good job")
                self.currentMoney += stake * 10
                self.gameWidget.currentMoney.setText(str(self.currentMoney))
			    #하나만 체크해도 됨.
                if self.slotValue[0] == 7:
                    self.gameWidget.statusBar.setText("Jack pot!")
                    print("Jack pot!")
                    self.currentMoney += stake * 100
                    self.gameWidget.currentMoney.setText(str(self.currentMoney))
            elif self.slotValue[0] ==  self.slotValue[1] or self.slotValue[0] == self.slotValue[2] or self.slotValue[1] == self.slotValue[2]:
                self.currentMoney += stake * 3
                self.gameWidget.currentMoney.setText(str(self.currentMoney))
                self.gameWidget.statusBar.setText("luckyyy!")
                print("luckyyy!")
            else:
                self.gameWidget.statusBar.setText("kkwang!")
                print("kkwang!")

        elif key == 'New Game':
            print("new game")
            self.gameWidget.stake.clear()
            self.gameWidget.currentMoney.setText(str(self.currentMoney))
            self.currentMoney = 1000
            self.gameWidget.currentMoney.setText(str(self.currentMoney))

            self.currentTrial = 5
            self.gameWidget.count.setText(str(self.currentTrial))
            for i in range(len(self.slotValue)):
                self.gameWidget.outputs[i].clear()
                self.slotValue = [None, None, None]



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gameWindow = mainWindow()
    gameWindow.show()
    sys.exit(app.exec_())
