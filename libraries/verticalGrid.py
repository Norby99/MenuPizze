from libraries.database import database
import tkinter as tk
from libraries.gridNewColumn import NewColumnCell
from libraries.windowSpecs import WindowSpecs

class VerticalGrid:
    def __init__(self, cells, margini, dbData, maxColumns=5):
        """
        Defines a vertical grid that show some cell
        @maxRows if defined, sets a max height for all cells (default to False)
        """
        self.cells = cells
        self.maxColumns = maxColumns
        self.margin = margini

        self.db = database("localhost", dbData["dbUserName"], dbData["dbPassword"], dbData["dbData"])

    def show(self, update=False):
        if update:
            self.updateScritte()
        else:
            cellPosition = [self.margin[0], self.margin[1]]
            for object in self.cells:
                object.setPostion(cellPosition)
                cellPosition[1] = object.getBottomCoordinate()

                prevObject = object
                if prevObject.getBottomCoordinate() > self.margin[3]: # getting next element position
                    cellPosition = [prevObject.getRightCoordinate(), self.margin[1]]

                if object.getRightCoordinate() > self.margin[2]:
                    raise IndexError("Given too many Cell's")

    def updateCells(self):    #this function updates the text boxes
        testoLingua = self.getLingua()

        for i in self.cells:
            if hasattr(i, 'update'):
                i.update(testoLingua)

    def getLingua(self):
        return self.db.getCurrentLanguage()
