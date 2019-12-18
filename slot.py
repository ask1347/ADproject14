import random


class Slot:

    def roll():
        result = []
        for i in range(3):
            result.append(random.randint(0,9))
        return result
        

    def reward(self):
            # 숫자 두개가 맞을경우

            if self.slotValue[0] == self.slotValue[1] or self.slotValue[0] == self.slotValue[2] or self.slotValue[1] == self.slotValue[2]:
                m = m - s + s*2
            # 숫자 세개가 다 일치할 경우와 777이 발생할 경우
            elif self.slotValue[0] == self.slotValue[1] and self.slotValue[0] == self.slotValue[2]:
                m = m - s + s*3
            elif self.slotValue[0] == self.slotValue[1] and self.slotValue[0] == self.slotValue[2] and self.slotValue[0] == 7:
                m = m - s + s*5
            #하나도 맞지 않았을 경우
            else:
                m = m - s
            #근데 이거 안쓰고 slotgame에 bet 키에 붙임


    def moneyFinished(self):
        if money <= 0:
            return True
        elif money >= 10000:
            return True

    def countFinished(self):
        if count <= 0:
            return True
        elif count >= 0:
            return False
