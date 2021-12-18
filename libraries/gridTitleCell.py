from libraries.gridCell import Cell

class TitleCell(Cell):
    """ This cell contains a big title and a border """

    def __init__(self, canvas, position, dimensions, title):
        super().__init__(canvas, position, dimensions)
        self.title = title
        self.setTitle(self.title)
        self.setBorders()

    def setTitle(self, title):
        self.title = title

    def setBorders(self):
        self.canvas.create_line(self.relativeXPostion(0), self.relativeYPostion(0), self.relativeXPostion(-1)-self.windowSpecs.resolutionConverter(40), self.relativeYPostion(0), fill="#ff8000", width="3")
        self.canvas.create_line(self.relativeXPostion(0), self.relativeYPostion(-1)-self.windowSpecs.resolutionConverter(15), self.relativeXPostion(-1)-self.windowSpecs.resolutionConverter(40), self.relativeYPostion(-1)-self.windowSpecs.resolutionConverter(15), fill="#ff8000", width="3")
