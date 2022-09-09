from libraries.pizzaHandler import Pizzas
from libraries.utils.utils import waitForConnection
from libraries.verticalGrid import VerticalGrid
from libraries.pizzaMenu import PizzaMenu
from libraries.utils.languageHandler import LanguageHandler

class PizzaMenu1(PizzaMenu):

    def __init__(self):
        data = self.loadJsonData("setup.json")
        dbData = self.loadJsonData("DBsetup.json")
        self.LHandler = LanguageHandler(dbData['languageSite'] + "/" + dbData['restaurantName'] + ".php", dbData['defaultLanguage'], token=dbData['m_key'], no_connection=True)
        self.pizza = Pizzas(dbData)
        self.pizzaTypesRequered = ["Pizze classiche", "Pizze bianche", "Pizze conditissime"] # the pizza types that have to be visualized
        #self.pizza.downloadAllFromCloud(force=True)
        self.pizza.loadPizzasFromJson()
        
        self.tkWindowSetup()

        ### These are all the pretty combinations I've found
        #colors = {"background" : "#003049", "generic_text" : "#EAE2B7", "titolo" : "#FCBF49","price" : "#D62828", "p_tipo" : "#F77F00","p_classica" : "#FF0000", "p_bianca" : "#0000FF", "p_speciale" : "#FF0000"}
        #colors = {"background" : "#000000", "p_tipo" : "#FCA311", "titolo" : "#14213D", "generic_text" : "#E5E5E5", "price" : "#FFFFFF"}
        #colors = {"background" : "#1D3557", "p_tipo" : "#E63946", "titolo" : "#F1FAEE", "generic_text" : "#A8DADC", "price" : "#457B9D"}
        #colors = {"background" : "#F4F1DE", "p_tipo" : "#E07A5F", "titolo" : "#3D405B", "generic_text" : "#81B29A", "price" : "#F2CC8F"}
        #colors = {"background" : "#3D405B", "p_tipo" : "#E07A5F", "titolo" : "#81B29A", "generic_text" : "#F4F1DE", "price" : "#F2CC8F"}
        #colors = {"background" : "#2b2e4a", "p_tipo" : "#E07A5F", "titolo" : "#81B29A", "generic_text" : "#F4F1DE", "price" : "#F2CC8F"}
        #colors = {"background" : "#2b2e4a", "p_tipo" : "#e84545", "titolo" : "#903749", "generic_text" : "#53354a", "price" : "#903749"}
        #colors = {"background" : "#540B0E", "p_tipo" : "#e84545", "titolo" : "#E09F3E", "generic_text" : "#FFF3B0", "price" : "#335C67"}
        #colors = {"background" : "#2B2D42", "p_tipo" : "#EF233C", "titolo" : "#8D99AE", "generic_text" : "#EDF2F4", "price" : "#EF233C"}598392
        #colors = {"background" : "#0B0014", "p_tipo" : "#FFFFFF", "titolo" : "#ef233c", "generic_text" : "#F5E9E2", "price" : "#fdc500"}
        colors = data["colors"] # colors are taken from the setup file
        self.setFontColors(colors)
        padding = 20
        self.window.configure(background=colors["background"])

        gridColumns = 5
        gridPosition = (self.windowSpecs.resolutionConverter(padding), self.windowSpecs.resolutionConverter(padding), self.windowSpecs.getScreenDimension()[0]-self.windowSpecs.resolutionConverter(padding), self.windowSpecs.getScreenDimension()[1]-self.windowSpecs.resolutionConverter(padding))
        self._columnWidth = (gridPosition[2]-gridPosition[0])/gridColumns

        self.allergens = self.loadAllergeni()
        pizze = self.pizzeCreator(self.pizzaTypesRequered)
        
        cells = pizze

        menu = VerticalGrid(cells, gridPosition, self.LHandler, maxColumns=2)

        self.show(menu)
        self.update()
        self.window.mainloop()

if __name__ == '__main__':
    waitForConnection()
    app = PizzaMenu1()
