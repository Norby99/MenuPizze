from libraries.cells.AbstractCell import Cell
import tkinter as tk
import tkinter.font as TkFont

class MenuSettimanaCell(Cell):
    
    def __init__(self, window, day, meal, price, position, width, proportion=5.76) -> None:
        """
            Parameters
            ----------
            day : str
                the day of the week
            meal : str
                The body of the cell
            price : str
                The price of the meal
            position : list
                The position of the cell
            width : float
                The width of the cell
            proportion : float, optional
                The proportion between the width and the height of the cell, by default 5.76
        """
        super().__init__(window, position, width, proportion)

        # TODO: try to make the body of the cell scalable with the height of the text
