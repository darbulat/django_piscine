#!/usr/bin/python3

class HotBeverage:
    def __init__(self):
        self.price = 0.30
        self.name = "hot beverage"
        self._description = "Just some hot water in a cup."

    def description(self) -> str:
        return self._description

    def __str__(self) -> str:
        return f"name : {self.name}\nprice : {self.price:0.2f}\ndescription : {self.description()}"


class Coffee(HotBeverage):
    def __init__(self):
        self.name = "coffee"
        self.price = 0.40
        self._description = "A coffee, to stay awake."


class Tea(HotBeverage):
    def __init__(self):
        self.name = "tea"
        self.price = 0.30
        self._description = "Just some hot water in a cup"


class Chocolate(HotBeverage):
    def __init__(self):
        self.name = "chocolate"
        self.price = 0.50
        self._description = "Chocolate, sweet chocolate..."


class Cappuccino(HotBeverage):
    def __init__(self):
        self.name = "cappuccino"
        self.price = 0.45
        self._description = "Un po’ di Italia nella sua tazza!"
