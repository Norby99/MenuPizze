from libraries.pizzaMenu import PizzaMenu
from libraries.resourceHandler import Recources
from libraries.utils.utils import waitForConnection
from libraries.verticalGrid import VerticalGrid
from libraries.utils.languageHandler import LanguageHandler
from libraries.repository.db_setup.dataReader import DataReader
from libraries.colors import Colors

class PizzaMenu2(PizzaMenu):

    def __init__(self):
        dbData = DataReader()
        self.LHandler = LanguageHandler(dbData.getWebsite(), dbData.getDefaultLanguage(), token=dbData.getToken(), no_connection=False)
        self.resources = Recources(dbData)
        self.pizzaTypesRequered = ["Impasto Napoletano", "Pizze Dolci"] # the pizza types that have to be visualized
        self.resources.downloadAllFromCloud(force=True)
        
        self.tkWindowSetup()
        colors = Colors()   # colors are taken from the setup file
        padding = 20
        self.window.configure(background=colors.background)

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
