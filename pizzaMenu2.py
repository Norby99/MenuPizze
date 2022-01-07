from libraries.pizzaMenu import PizzaMenu
from libraries.PizzaHandler import Pizzas
from libraries.utils import waitForConnection
from libraries.windowSpecs import WindowSpecs
from libraries.verticalGrid import VerticalGrid

class PizzaMenu2(PizzaMenu):

    def __init__(self):
        data = self.loadSetupData()
        self.pizza = Pizzas(data)
        self.pizzaTypesRequered = ["Impasto Napoletano", "Pizze Dolci"] # the pizza types that have to be visualized
        self.pizza.downloadAllFromCloud()
        
        self.tkWindowSetup()
        colors = data["colors"] # colors are taken from the setup file
        padding = 20
        menuMaxColumns = 4
        self.window.configure(background=colors["background"])

        pizze = self.pizzeCreator(self.pizzaTypesRequered)
        aggiunte = self.aggiunteCreator()
        insalate = self.insalateCreator()
        elements = pizze + aggiunte

        firstGridColumns = 2    # first menu part generator
        firstGridPosition = (self.windowSpecs.resolutionConverter(padding), self.windowSpecs.resolutionConverter(padding), self.windowSpecs.getScreenDimension()[0]*firstGridColumns/menuMaxColumns, self.windowSpecs.getScreenDimension()[1]-self.windowSpecs.resolutionConverter(padding))
        cells1 = self.createCells(elements, colors, (firstGridPosition[2]-firstGridPosition[0])/firstGridColumns)

        secondGridColumns = 1    # second menu part generator
        secondGridPosition = (firstGridPosition[2], self.windowSpecs.resolutionConverter(padding), self.windowSpecs.getScreenDimension()[0]*secondGridColumns/menuMaxColumns+firstGridPosition[2], self.windowSpecs.getScreenDimension()[1]-self.windowSpecs.resolutionConverter(padding))
        cells2 = self.createCells(insalate, colors, (secondGridPosition[2]-secondGridPosition[0])/secondGridColumns)

        menuPizze = VerticalGrid(cells1, firstGridPosition, data, maxColumns=firstGridColumns)  # creating the menu part
        menuInsalate = VerticalGrid(cells2, secondGridPosition, data, maxColumns=secondGridColumns)

        menu = [menuPizze, menuInsalate]

        self.show(menu)
        self.update(menu)
        self.window.mainloop()

if __name__ == '__main__':
    waitForConnection()
    app = PizzaMenu2()
