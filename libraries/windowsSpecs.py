import tkinter

class WindowSpecs:

    def __init__(self):
        root = tkinter.Tk()
        self.screenDimension = root.winfo_screenwidth(), root.winfo_screenheight()
        root.quit()
        root.destroy()

    def getScreenDimension(self):
        """ Returns a tuple containing the resolution of the display """
        return self.screenDimension

    def resolutionConverter(self, n):
        """Converts the ratio from 2560x1440 to ris"""
        return int(n/(2560/self.screenDimension[0]))

if __name__ == "__main__":
    w = WindowSpecs()
    print(w.getScreenDimension())
