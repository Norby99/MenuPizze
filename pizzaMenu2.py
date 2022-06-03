from libraries.pizzaMenu import PizzaMenu
from libraries.pizzaHandler import Pizzas
from libraries.utils.utils import waitForConnection
from libraries.verticalGrid import VerticalGrid
from libraries.utils.languageHandler import LanguageHandler

class PizzaMenu2(PizzaMenu):

    def __init__(self):
        data = self.loadJsonData("setup.json")
        dbData = self.loadJsonData("DBsetup.json")
        self.LHandler = LanguageHandler(dbData['languageSite'] + "/" + dbData['restaurantName'] + ".php", dbData['defaultLanguage'], token=dbData['m_key'], no_connection=True)
        self.pizza = Pizzas(dbData)
        self.pizzaTypesRequered = ["Impasto Napoletano", "Pizze Dolci"] # the pizza types that have to be visualized
        self.pizza.downloadAllFromCloud(force=True)
        
        self.tkWindowSetup()
        colors = data["colors"] # colors are taken from the setup file
        padding = 20
        self.window.configure(background=colors["background"])

        pizze = self.pizzeCreator(self.pizzaTypesRequered)
        aggiunte = self.aggiunteCreator()
        insalate = self.insalateCreator()
        allergeni = self.loadAllergeni()
        logo = self.logoCreator()
        social_logos = self.loadSocialLogos()
        allergeniObj = self.allergeniCreator()
        coperto = self.simpleTextCreator(["Consumazione sul posto 0.50€"])

        elements = pizze + aggiunte + self.DEFAULT_NEWLINE + insalate + self.DEFAULT_NEWLINE + logo + social_logos + allergeniObj + coperto

        gridColumns = 4
        gridPosition = (self.windowSpecs.resolutionConverter(padding), 0, self.windowSpecs.getScreenDimension()[0]-self.windowSpecs.resolutionConverter(padding), self.windowSpecs.getScreenDimension()[1])
        cells = self.createCells(elements, allergeni, colors, (gridPosition[2]-gridPosition[0])/gridColumns)

        menu = VerticalGrid(cells, gridPosition, self.LHandler, maxColumns=gridColumns)

        self.show(menu)
        self.update()
        self.window.mainloop()

if __name__ == '__main__':
    waitForConnection()
    app = PizzaMenu2()
