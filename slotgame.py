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
        self.Xoutput = QLineEdit(self)
        self.Xoutput.setReadOnly(True)
        self.Youtput = QLineEdit(self)
        self.Youtput.setReadOnly(True)
        self.Zoutput = QLineEdit(self)
        self.Zoutput.setReadOnly(True)

        outputLayout = QGridLayout()
        outputLayout.addWidget(self.Xoutput, 0, 1, 1, 1)
        outputLayout.addWidget(self.Youtput, 0, 2, 1, 1)
        outputLayout.addWidget(self.Zoutput, 0, 3, 1, 1)

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
        self.Stake = QLineEdit()
        self.Count = QLineEdit("남은 횟수: ", self)
        self.Count.setReadOnly(True)
        self.statusBar = QLineEdit("상태: ", self)
        self.statusBar.setReadOnly(True)

        userLayout = QGridLayout()
        userLayout.addWidget(self.betButton, 0, 0)
        userLayout.addWidget(self.newGameButton, 1, 0)
        userLayout.addWidget(self.currentMoneyLabel, 0, 1)
        userLayout.addWidget(self.currentMoney, 0, 2)
        userLayout.addWidget(self.stakeLabel, 1, 1)
        userLayout.addWidget(self.Stake, 1, 2)
        userLayout.addWidget(self.Count, 2, 0)
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

        #
        money = 1000
        self.gameWidget.currentMoney.setText(str(money))
        self.gameWidget.Stake.setText('')

        # Initialize a new game
        self.game = Slot()
        self.slotValue = []
        self.stake = 0
        count = 10
        self.currentmoney = money


    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if key == 'Bet':
            print("Betting")
            self.gameOver = False
            self.gameWidget.Stake.clear()

            self.slotValue = Slot.roll()
            self.gameWidget.Xoutput.setText(str(self.slotValue[0]))
            self.gameWidget.Youtput.setText(str(self.slotValue[1]))
            self.gameWidget.Zoutput.setText(str(self.slotValue[2]))
            s = 0
            s = self.stake
            #보상 계산
            if self.slotValue[0] == self.slotValue[1] or self.slotValue[0] == self.slotValue[2] or self.slotValue[1] == self.slotValue[2]:
                currentmoney = 0 - s + s*2
            # 숫자 세개가 다 일치할 경우와 777이 발생할 경우
            elif self.slotValue[0] == self.slotValue[1] and self.slotValue[0] == self.slotValue[2]:
                currentmoney = 0 - s + s*3
            elif self.slotValue[0] == self.slotValue[1] and self.slotValue[0] == self.slotValue[2] and self.slotValue[0] == 7:
                currentmoney = 0 - s + s*10
            #하나도 맞지 않았을 경우
            else:
                currentmoney = 0 - s

            self.gameWidget.currentMoney.setText(str(currentmoney))


        elif key == 'New Game':
            print("new game")
            self.currentmoney = 1000
            Count = 10
            self.gameWidget.Stake.clear()
            self.gameWidget.Xoutput.setText('')
            self.gameWidget.Youtput.setText('')
            self.gameWidget.Zoutput.setText('')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gameWindow = mainWindow()
    gameWindow.show()
    sys.exit(app.exec_())
