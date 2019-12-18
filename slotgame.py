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
        userLayout.addWidget(self.count, 2, 0, 1, 0)
        userLayout.addWidget(self.statusBar, 2, 1, 1, 3)

        # main Layout
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
            #bet버튼 구현
        if key == 'Bet':
            print("Betting")
            #실행횟수가 없을 때 메시지와 함께 게임진행이 안되도록
            if self.currentTrial <= 0:
                print("No trial left")
                self.gameWidget.statusBar.setText("No trial left")
                return
            self.gameWidget.count.setText("Left trials: " + str(self.currentTrial))

            try:
                stake = int(self.gameWidget.stake.text())
                if stake > 0:
                    self.currentMoney -= stake
                    self.gameWidget.currentMoney.setText(str(self.currentMoney))
                    self.currentTrial -= 1
                    self.gameWidget.count.setText("Left trials: " + str(self.currentTrial))
                    #판돈을 걸지않거나 음수,숫자이외의 것을 입력할시 막는 기능
                elif stake < 0:
                    print("You can't bet negative number")
                    self.gameWidget.statusBar.setText("You can't bet negative number")
                    return
                elif stake == 0:
                    print("You can't bet for free")
                    self.gameWidget.statusBar.setText("You can't bet for free")
                    return
            except ValueError as e:
                print("there is no stake value")
                self.gameWidget.statusBar.setText("There is no stake value")
                return

            self.gameWidget.stake.clear()
                #버튼을 누르면 랜덤하게 슬롯 설정 (0~999)
            self.slotValue = Slot.roll()
            for i in range(len(self.slotValue)):
                self.gameWidget.outputs[i].setText(str(self.slotValue[i]))
                #보상 및 계산
            if self.slotValue[0] == self.slotValue[1] and self.slotValue[0] == self.slotValue[2]:
                self.gameWidget.statusBar.setText("good job")
                print("good job")
                self.currentMoney += stake * 10
                self.gameWidget.currentMoney.setText(str(self.currentMoney))
                #777의 경우 특별처리
                if  self.slotValue[0] == 7:
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
        # New Game 버튼 구현
        elif key == 'New Game':
            print("new game")
            #stake와 money를 초기화
            self.gameWidget.stake.clear()
            self.gameWidget.currentMoney.setText(str(self.currentMoney))
            self.currentMoney = 1000
            self.gameWidget.currentMoney.setText(str(self.currentMoney))
            self.gameWidget.statusBar.setText("status")
            # 시도 횟수를 초기화
            self.currentTrial = 5
            self.gameWidget.count.setText(str(self.currentTrial))
            # 슬롯 초기화
            for i in range(len(self.slotValue)):
                self.gameWidget.outputs[i].clear()
                self.slotValue = [None, None, None]

        # 돈이 0원 이하로 떨어질때 게임오버
        if self.currentMoney <= 0:
            self.currentTrial = 0
            self.gameWidget.count.setText("Left trials: " + str(self.currentTrial))
            print("You're bankrupt.")
            self.gameWidget.statusBar.setText("You're bankrupt.Start new game.")
            return
        # 돈이 100000원 이상으로 늘어날때 게임클리어
        elif self.currentMoney >= 100000:
            self.currentTrial = 0
            self.gameWidget.count.setText("Left trials: " + str(self.currentTrial))
            print("Congratulations! You won!")
            self.gameWidget.statusBar.setText("Congratulations! You won!")
            return

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gameWindow = mainWindow()
    gameWindow.show()
    sys.exit(app.exec_())
