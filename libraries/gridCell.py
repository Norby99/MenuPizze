from libraries.windowSpecs import WindowSpecs
from abc import ABC

class Cell(ABC):

    def __init__(self, canvas, position, dimensions, winInfoBase=False):
        """screenDim is an object that is used to avoid creating a tkinter class every time"""
        self.position = position
        self.dimensions = dimensions
        self.canvas = canvas
        if winInfoBase:
            self.windowSpecs = winInfoBase
        else:
            self.windowSpecs = WindowSpecs()

    def relativeXPostion(self, pos):
        """Returns the relative X position of a given coordinate"""
        if pos >= 0:
            return self.position[0]+pos
        else:
            return self.position[0]+self.dimensions[0]+pos

    def relativeYPostion(self, pos):
        """Returns the relative Y position of a given coordinate"""
        if pos >= 0:
            return self.position[1]+pos
        else:
            return self.position[1]+self.dimensions[1]+pos
