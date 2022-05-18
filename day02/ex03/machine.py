#!/usr/bin/python3

import random
from beverages import HotBeverage, Coffee, Tea, Cappuccino, Chocolate


class CoffeeMachine:

    class EmptyCup(HotBeverage):
        def __init__(self):
            super().__init__()
            self.name = "empty cup"
            self.price = 0.90
            self._description = "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def __init__(self):
        self.broken_count = 10

    def repair(self):
        self.broken_count = 10

    def serve(self, drink: HotBeverage) -> HotBeverage:
        if self.broken_count <= 0:
            raise CoffeeMachine.BrokenMachineException
        self.broken_count -= 1
        if random.randint(0, 5) == 0:
            return CoffeeMachine.EmptyCup()
        return drink()


def test():
    coffee_machine = CoffeeMachine()
    for i in range(22):
        print(i)
        try:
            print(coffee_machine.serve(
                random.choice([Coffee, Tea, Cappuccino, Chocolate]))
            )
        except CoffeeMachine.BrokenMachineException as e:
            print(e)
            coffee_machine.repair()


if __name__ == '__main__':
    test()
