import random
n=random.randint(0,999)
x = n// 100
y = n// 10 - 10*x
z = n% 10
#각각 n의 100,10,1의 자리의 숫자

class Slot:

    def slotrank(self):
        #숫자 두개가 맞을경우
        if x == y or x == z or y==z:
            return 1
        #숫자 세개가 다 일치할 경우와 777이 발생할 경우
        elif x == y and x == z:
            if x == 7:
                return 3
            else: return 2
        else: return 0

    def stake():
        m = 0
        s = 0
        m = currentMoney
        s = Stake
        if m >= s:
            if slotrank() == 0:
                m = m - s
            elif slotrank() == 1:
                m = m - s + s*2
            elif slotrank() == 2:
                m = m - s + s*3
            elif slotrank() == 3:
                m = m - s + s*5
        else: print("돈이 부족합니다.")

    def newGame(self, count):

        self.trials = 0