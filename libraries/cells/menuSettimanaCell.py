from libraries.cells.AbstractCell import Cell
import tkinter as tk
import tkinter.font as TkFont

class MenuSettimanaCell(Cell):
    
    def __init__(self, window, title, rows, position, width, proportion=5.76) -> None:
        """
            Parameters
            ----------
            title : str
                The title of the cell
            rows : list[str]
                The body of the cell
        """
        super().__init__(window, position, width, proportion)
