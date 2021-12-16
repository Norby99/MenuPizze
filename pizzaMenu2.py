from pizzaMenu import PizzaMenu
from libraries.utils import capfirst, waitForConnection

class PizzaMenu2(PizzaMenu):

    def __init__(self):
        pass

if __name__ == '__main__':
    waitForConnection()
    app = PizzaMenu2()
