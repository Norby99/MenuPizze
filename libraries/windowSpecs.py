import tkinter

class WindowSpecs:

    def __init__(self, dimensions=[0,0]):
        if dimensions == [0,0]:
            root = tkinter.Tk()
            self.screenDimension = root.winfo_screenwidth(), root.winfo_screenheight()

            proportion = self.screenDimension[0]/self.screenDimension[1]
            if not (1 < proportion < 2) :  # if the screen resolution isn't between 4:3 and 16:9 (for example a 32:9)
                self.screenDimension[0] = int(self.screenDimension[0]/2)

            root.quit()
            root.destroy()
        else:
            self.screenDimension = dimensions

    def getScreenDimension(self):
        """ Returns a tuple containing the resolution of the display """
        return self.screenDimension

    def resolutionConverter(self, n):
        """Converts the ratio from 2560x1440 to ris"""
        return int(n/(2560/self.screenDimension[0]))

if __name__ == "__main__":
    w = WindowSpecs()
    print(w.getScreenDimension())
