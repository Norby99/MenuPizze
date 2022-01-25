from libraries.utils.cloud import Cloud
import json
from os import path
from libraries.utils.database import database, saveJsonFile
from libraries.utils.utils import fileIsOld

class Pizzas():
    """
    This class handles the pizzas:
    - downloads the json files from the website
    - reads the pizzas from the json files
    """
    def __init__(self, jsonData):
        self.data = jsonData
        self.cloud = Cloud(self.data["m_key"])

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
                self.loadPizzasFromJson()

    def loadPizzasFromJson(self):
        with open(self.filePathInResources('pizze.json')) as f:
            self.ElencoPizze = json.load(f)
        with open(self.filePathInResources('ingredienti.json')) as f:
            self.ElencoIngredienti = json.load(f)
        with open(self.filePathInResources('aggiunte.json')) as f:
            self.ElencoAggiunte = json.load(f)
        with open(self.filePathInResources('insalate.json')) as f:
            self.ElencoInsalate = json.load(f)

    def effectiveDownload(self):
        print("Downloading the files from the cloud...")
        self.ElencoPizze = self.cloud.read(self.data["pizze"])

        if self.ElencoPizze:    # if the server is responding
            self.ElencoIngredienti = self.cloud.read(self.data["ingredienti"])
            self.ElencoAggiunte = self.cloud.read(self.data["aggiunte"])
            self.ElencoInsalate = self.cloud.read(self.data["insalate"])

            print(self.filePathInResources("pizze.json"))
            saveJsonFile(self.filePathInResources("pizze.json"), self.ElencoPizze)
            saveJsonFile(self.filePathInResources("ingredienti.json"), self.ElencoIngredienti)
            saveJsonFile(self.filePathInResources("aggiunte.json"), self.ElencoAggiunte)
            saveJsonFile(self.filePathInResources("insalate.json"), self.ElencoInsalate)

            self.ElencoPizze = json.loads(self.ElencoPizze)
            self.ElencoIngredienti = json.loads(self.ElencoIngredienti)
            self.ElencoAggiunte = json.loads(self.ElencoAggiunte)
            self.ElencoInsalate = json.loads(self.ElencoInsalate)
        else:   # if the server is not responding
            self.loadPizzasFromJson()

    def uploadAll(self):
        """
        Deprecated!
        This method uploads the DB data to a website
        """
        db = database("localhost", self.data["dbUserName"], self.data["dbPassword"], self.data["dbData2BeUploaded"])
        queryPizze = ("""
            SELECT pizze.id, nomePizza, nome_tipo, prezzo, GROUP_CONCAT(`pizza-ingredienti`.`id_ingrediente` ORDER BY `pizza-ingredienti`.`id_collegamento`) AS "ingredienti"
            FROM pizze
            INNER JOIN tipo_pizze ON tipo_pizze.id_tipo = pizze.id_tipo
            INNER JOIN `pizza-ingredienti` ON pizze.id = `pizza-ingredienti`.id_pizza
            GROUP BY nomePizza
            ORDER BY pizze.id
        """)
        dbPizzaList = db.readByQuery(queryPizze, "json")
        self.cloud.update(dbPizzaList, self.data["pizze"])

        #uploadda gli ingredienti
        queryingredienti = ("""
            SELECT *
            FROM `ingredienti`
        """)
        dbIngredientsList = db.readByQuery(queryingredienti, "json")
        self.cloud.update(dbIngredientsList, self.data["ingredienti"])
        #uploadda le aggiunte
        queryAggiunte = ("""
            SELECT *
            FROM `aggiunte`
        """)
        dbAggiunteList = db.readByQuery(queryAggiunte, "json")
        self.cloud.update(dbAggiunteList, self.data["aggiunte"])

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
    """p = Pizzas("setup.json")
    p.downloadAllFromCloud()"""

    #la seguente parte di codice mi servira per uploaddare il menu modificato
    p = Pizzas("setup.json")
    p.uploadAll()
