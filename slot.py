import random


class Slot:

    def roll():
        result = []
        for i in range(3):
            result.append(random.randint(0,9))
        return result

    def moneyFinished(self):
        if currentMoney <= 0:
            print("You're bankrupt.")
            self.gameWidget.statusBar.setText("You're bankrupt.")
            return True
        elif currentMoney >= 100000:
            print("Congratulations! You won!")
            self.gameWidget.statusBar.setText("Congratulations! You won!")
            return True
        else:
            return False


