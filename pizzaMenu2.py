from pizzaMenu import PizzaMenu
from libraries.PizzaHandler import Pizzas
from libraries.utils import waitForConnection, waitForFilesUpdate
from libraries.windowSpecs import WindowSpecs
from libraries.verticalGrid import VerticalGrid

class PizzaMenu2(PizzaMenu):

    def __init__(self):
        data = self.loadSetupData()
        self.pizza = Pizzas(data)
        self.pizzaTypesRequered = ["Impasto Napoletano", "Pizze Dolci"] # the pizza types that have to be visualized
        waitForFilesUpdate()    # files are downloaded from the pizzaMenu2, so this class waits for the update
        self.pizza.loadPizzasFromJson()
        
        self.tkWindowSetup()
        self.windowSpecs = WindowSpecs()
        colors = data["colors"] # colors are taken from the setup file

        self.pizze = self.pizzeCreator(self.pizzaTypesRequered)
        self.menu = VerticalGrid(self.window, self.pizze, [self.windowSpecs.resolutionConverter(25), self.windowSpecs.resolutionConverter(25), self.windowSpecs.getScreenDimension()[0]-self.windowSpecs.resolutionConverter(25), self.windowSpecs.getScreenDimension()[1]-self.windowSpecs.resolutionConverter(25)], data, colors)

        self.ShowAll()
        self.Update()
        self.window.mainloop()

if __name__ == '__main__':
    waitForConnection()
    app = PizzaMenu2()
