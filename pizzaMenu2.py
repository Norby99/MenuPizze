from libraries.pizzaMenu import PizzaMenu
from libraries.resourceHandler import Recources
from libraries.utils.utils import waitForConnection
from libraries.verticalGrid import VerticalGrid
from libraries.utils.languageHandler import LanguageHandler

class PizzaMenu2(PizzaMenu):

    def __init__(self):
        data = self.loadJsonData("setup.json")
        dbData = self.loadJsonData("DBsetup.json")
        self.LHandler = LanguageHandler(dbData['languageSite'] + "/" + dbData['restaurantName'] + ".php", dbData['defaultLanguage'], token=dbData['m_key'], no_connection=False)
        self.resources = Recources(dbData)
        self.pizzaTypesRequered = ["Impasto Napoletano", "Pizze dolci"] # the pizza types that have to be visualized
        self.resources.downloadAllFromCloud(force=True)
        
        self.tkWindowSetup()
        colors = data["colors"] # colors are taken from the setup file
        self.setFontColors(colors)
        padding = 20
        self.window.configure(background=colors["background"])

        gridColumns = 4
        gridPosition = (self.windowSpecs.resolutionConverter(padding), 0, self.windowSpecs.getScreenDimension()[0]-self.windowSpecs.resolutionConverter(padding), self.windowSpecs.getScreenDimension()[1])
        self._columnWidth = (gridPosition[2]-gridPosition[0])/gridColumns

        self.allergens = self.loadAllergeni()
        cells = self.cellsElementsGetter()

        menu = VerticalGrid(cells, gridPosition, self.LHandler, maxColumns=gridColumns)

        self.show(menu)
        self.update()
        self.window.mainloop()

    def cellsElementsGetter(self):
        pizze = self.pizzeCreator(self.pizzaTypesRequered)
        aggiunte = self.aggiunteCreator()
        insalate = self.insalateCreator()
        logo = self.logoCreator()
        social_logos = self.loadSocialLogos()
        allergeniObj = self.allergeniCreator()
        coperto = self.simpleTextCreator(["Consumazione sul posto 0.50€"])
        menuSettimana = self.menuSettimanaCreator()

        return pizze + aggiunte + self.newColumnCreator() + insalate + menuSettimana + self.newColumnCreator() + logo + social_logos + allergeniObj + coperto

if __name__ == '__main__':
    waitForConnection()
    app = PizzaMenu2()
