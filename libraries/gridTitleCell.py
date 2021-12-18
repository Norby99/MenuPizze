from libraries.gridCell import Cell

class TitleCell(Cell):

    def __init__(self, position, dimensions, title):
        super().__init__(position, dimensions)
        self.title = title
        self.setTitle(self.title)

    def setTitle(self, title):
        self.title = title
