from abc import ABC

class Cell(ABC):

    def __init__(self, position, dimensions):
        self.position = position
        self.dimensions = dimensions
