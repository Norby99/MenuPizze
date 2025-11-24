from libraries.utils.cloud import Cloud
import json
from os import path
from libraries.utils.database import saveJsonFile
from libraries.utils.utils import fileIsOld
from libraries.utils.logger import Logger

class Recources():
    """
    This class handles the pizzas:
    - downloads the json files from the website
    - reads the pizzas from the json files
    """

    _logger: Logger

    def __init__(self, dbData):
        self.data = dbData
        self.cloud = Cloud(self.data.getToken())
        self._logger = Logger()

    def downloadAllFromCloud(self, force=False):
        """
        Checks if the files are too old and then downloads all from the cloud and creats the json files
        @param force : if True, download the files even if the files aren't old
        """

        if force:
            self.effectiveDownload()
        else:
            if fileIsOld(self.filePathInResources("aggiunte.json")):
                self.effectiveDownload()
            else:
                self.loadAllFromJson()

    def loadAllFromJson(self):
        with open(self.filePathInResources('pizze.json')) as f:
            self.ElencoPizze = json.load(f)
        with open(self.filePathInResources('ingredienti.json')) as f:
            self.ElencoIngredienti = json.load(f)
        with open(self.filePathInResources('aggiunte.json')) as f:
            self.ElencoAggiunte = json.load(f)
        with open(self.filePathInResources('insalate.json')) as f:
            self.ElencoInsalate = json.load(f)
        with open(self.filePathInResources('menu-settimanale.json')) as f:
            self.MenuSettimanale = json.load(f)

    def effectiveDownload(self):
        self._logger.disp("Downloading the files from the cloud...")
        self.ElencoPizze = self.cloud.read(self.data.getPizze())
        self.ElencoIngredienti = self.cloud.read(self.data.getIngredienti())
        self.ElencoAggiunte = self.cloud.read(self.data.getAggiunte())
        self.ElencoInsalate = self.cloud.read(self.data.getInsalate())
        self.MenuSettimanale = self.cloud.read(self.data.getMenuSettimanale())
        if self.ElencoPizze and self.ElencoIngredienti and self.ElencoAggiunte and self.ElencoInsalate and self.MenuSettimanale:     # if the server is responding and the files are valid
            saveJsonFile(self.filePathInResources("pizze.json"), self.ElencoPizze)
            saveJsonFile(self.filePathInResources("ingredienti.json"), self.ElencoIngredienti)
            saveJsonFile(self.filePathInResources("aggiunte.json"), self.ElencoAggiunte)
            saveJsonFile(self.filePathInResources("insalate.json"), self.ElencoInsalate)
            saveJsonFile(self.filePathInResources("menu-settimanale.json"), self.MenuSettimanale)

        else:   # if the server is not responding or a file is not valid
            self._logger.disp("An error occured. An older version of files will be loaded.\nNote that if there was any donwloaded file, none of them will be saved.")
        
        self.loadAllFromJson()

    def get_pizzas(self, merge=False):
        """
        Gets all the pizzas and ingredients and merge them toghether
        """
        if merge:
            elencoEsteso = []
            for i in self.ElencoPizze:  #scorro le pizze
                elencoEsteso.append(i)
                ingredientiScritti = []
                ingredientiScrittiInglese = []
                ingredienti = i["ingredienti"]
                ingredienti = list(ingredienti.split(","))
                allergens = self.getAllergenByPizzaType(i["nome_tipo"]) # getting the allergens of the pizza dough
                for id_ingrediente in ingredienti:  #scorro gli ingredienti della pizza
                    for id_elencoIngrediente in self.ElencoIngredienti: #scorro tutti gli ingredienti
                        if int(id_elencoIngrediente["id_ingrediente"]) == int(id_ingrediente):
                            ingredientiScritti.append(id_elencoIngrediente["nome_italiano"])
                            ingredientiScrittiInglese.append(id_elencoIngrediente["nome_inglese"])
                            if id_elencoIngrediente["tipo"] != "Null":
                                allergens.add(id_elencoIngrediente["tipo"].lower())
                            
                elencoEsteso[-1]["ingredienti"] = ','.join(ingredientiScritti)
                elencoEsteso[-1]["ingredientiInglese"] = ','.join(ingredientiScrittiInglese)
                elencoEsteso[-1]["allergeni"] = allergens

            return elencoEsteso
        else:
            return self.ElencoPizze

    def get_insalate(self, merge=False):
        """
        Gets all the insalate and ingredients and merge them toghether
        """
        if merge:
            elencoEsteso = []
            for i in self.ElencoInsalate:  #scorro le pizze
                elencoEsteso.append(i)
                ingredientiScritti = []
                ingredientiScrittiInglese = []
                ingredienti = i["ingredienti"]
                ingredienti = list(ingredienti.split(","))
                allergens = set()
                for id_ingrediente in ingredienti:  #scorro gli ingredienti della pizza
                    for id_elencoIngrediente in self.ElencoIngredienti: #scorro tutti gli ingredienti
                        if int(id_elencoIngrediente["id_ingrediente"]) == int(id_ingrediente):
                            ingredientiScritti.append(id_elencoIngrediente["nome_italiano"])
                            ingredientiScrittiInglese.append(id_elencoIngrediente["nome_inglese"])
                            if id_elencoIngrediente["tipo"] != "Null":
                                allergens.add(id_elencoIngrediente["tipo"].lower())
                            
                elencoEsteso[-1]["ingredienti"] = ','.join(ingredientiScritti)
                elencoEsteso[-1]["ingredientiInglese"] = ','.join(ingredientiScrittiInglese)
                elencoEsteso[-1]["allergeni"] = allergens

            return elencoEsteso
        else:
            return self.ElencoPizze

    def get_menu_settimanale(self):
        """
        Gets menu settimanale
        """
        return self.MenuSettimanale

    def getAllergenByPizzaType(self, pizzaType):
        """
        Given a type of pizza, it returns a set of it's allergens
        """
        allergens = set()
        if pizzaType in ["Pizze classiche", "Pizze bianche", "Pizze conditissime", "Pizze Dolci"]:
            allergens.update(["glutine", "soia"])
        elif pizzaType in ["Impasto Napoletano"]:
            allergens.add("glutine")
        return allergens

    def get_aggiunte(self):
        return self.ElencoAggiunte

    def get_ingredienti(self):
        return self.ElencoIngredienti

    def filePathInResources(self, file):
        """ Return the absolute path of the given @file in the resource/pizzeJson folder """
        return path.join("resources", "pizzeJson", file)

if __name__ == "__main__":
    p = Recources("setup.json")
    p.downloadAllFromCloud()
