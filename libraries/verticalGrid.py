import tkinter as tk
from libraries.cells.newColumn import NewColumnCell

class VerticalGrid:
    def __init__(self, cells, margin, LHandler, maxColumns=5):
        """
        Defines a vertical grid that show some cell
        """
        self.cells = cells
        self.maxColumns = maxColumns
        self.margin = margin

        self.LHandler = LHandler

    def show(self, update=False):
        if update:
            self.updateScritte()
        else:
            cellPosition = [self.margin[0], self.margin[1]]
            for cell in self.cells:
                if isinstance(cell, NewColumnCell): # if the cell is of typo of NewColumnCell, it goes to the new column
                    cellPosition = [prevObject.getRightCoordinate(), self.margin[1]]
                    continue

                cell.setPostion(cellPosition)
                cellPosition[1] = cell.getBottomCoordinate()

                prevObject = cell
                if prevObject.getBottomCoordinate() > self.margin[3]: # getting next element position
                    cellPosition = [prevObject.getRightCoordinate(), self.margin[1]]

                if cell.getRightCoordinate() > self.margin[2]:
                    raise IndexError("Given too many Cell's")

    def updateCells(self):    #this function updates the text boxes
        testoLingua = self.getLingua()

        for i in self.cells:
            if hasattr(i, 'update'):
                i.update(testoLingua)

    def getLingua(self):
        return self.LHandler.getCurrentLanguage()
