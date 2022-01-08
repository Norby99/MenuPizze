from libraries.gridCell import Cell
import tkinter as tk

class NewColumnCell(Cell):
    """ This cell forces VerticalGrid to go to the next Column """

    def __init__(self, window, position, width):
        super().__init__(window, position, width, proportion=float("inf"))
