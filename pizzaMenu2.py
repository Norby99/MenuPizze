from pizzaMenu import PizzaMenu
from libraries.PizzaHandler import Pizzas
from libraries.utils import waitForConnection
from libraries.windowsSpecs import WindowSpecs

class PizzaMenu2(PizzaMenu):

    def __init__(self):
        data = self.loadSetupData()
        self.p = Pizzas(data)
        self.pizzaTypesRequered = ["Impasto Napoletano", "Pizze Dolci"] # the pizza types that have to be visualized

        self.p.downloadAllFromCloud()
        
        self.tkWindowSetup()
        self.windowSpecs = WindowSpecs(self.screenDimension)

if __name__ == '__main__':
    waitForConnection()
    app = PizzaMenu2()
