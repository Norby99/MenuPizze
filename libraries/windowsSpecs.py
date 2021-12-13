class WindowSpecs:

    def __init__(self, screenDimension):
        self.screenDimension = screenDimension

    #converts the ratio from 2560x1440 to ris
    def resolutionConverter(self, n):
        return int(n/(2560/self.screenDimension[0]))