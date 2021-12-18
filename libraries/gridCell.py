from abc import ABC

class Cell(ABC):

    def __init__(self, canvas, position, dimensions):
        self.position = position
        self.dimensions = dimensions
        self.canvas = canvas
