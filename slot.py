import random


class Slot:

    def roll():
        result = []
        for i in range(3):
            result.append(random.randint(0,9))
        return result



