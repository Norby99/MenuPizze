from libraries.gridCell import Cell
import tkinter as tk
import tkinter.font as TkFont

class PizzaCell(Cell):
    """
    This cell contains:
    - pizza name
    - price
    - ingredients
    - allergens
    """
    def __init__(self, window, name, nameColor, price, priceColor, ingredients, ingredientsColor, allergens, position, width, proportion=5.76):
        super().__init__(window, position, width, proportion)
        self.name = name    # name setup
        self.nameColor = nameColor
        self.nameFont = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(20), weight='bold')
        self.price = price  # price setup
        self.priceColor = priceColor
        self.priceFont = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(18), weight='bold')
        self.ingredients = ingredients  # ingredients setup
        self.ingredientsColor = ingredientsColor
        self.ingredientsFont = TkFont.Font(family="Times", size=self.windowSpecs.resolutionConverter(15))
        self.allergens = allergens

        self.createName()
        self.createPrice()
        self.createIngredients()
        self.showAllergeni()

    def createName(self):
        self.textName = self.canvas.create_text(self.windowSpecs.resolutionConverter(5), 0, anchor= tk.NW, fill=self.nameColor,font=self.nameFont, text=self.name)

    def createPrice(self):
        self.textPrice = self.canvas.create_text(self.dimensions[0]-self.windowSpecs.resolutionConverter(10), self.windowSpecs.resolutionConverter(5), anchor= tk.NE, fill=self.priceColor,font=self.priceFont, text=self.price)

    def createIngredients(self):
        self.textIngredients = self.canvas.create_text(self.windowSpecs.resolutionConverter(5), self.dimensions[1]/2-self.windowSpecs.resolutionConverter(13), anchor= tk.NW, fill=self.ingredientsColor,font=self.ingredientsFont, text=next(iter(self.ingredients)), width=(self.dimensions[0]-self.windowSpecs.resolutionConverter(5)))

    def showAllergeni(self):
        """ TkFont.Font(self.nameFont)
        print(self.nameFont.cget('width'))
        exit() """
        self.canvas.create_image(10, self.windowSpecs.resolutionConverter(5), anchor=tk.NW, image=self.allergens["glutine"])

    def setNameFont(self, font):
        self.nameFont = font

    def setPriceFont(self, font):
        self.priceFont = font

    def setIngredientsFont(self, font):
        self.ingredientsFont = font

    def update(self, language):
        self.canvas.itemconfig(self.textIngredients, text=self.ingredients[language])
