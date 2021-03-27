from cloud import Cloud
import json
import os
from datetime import datetime, time
from database import database, list2Json, saveJsonFile

class Pizzas():
    def __init__(self, fname):
        with open(fname) as f:
            self.data = json.load(f)
        self.c = Cloud(self.data["m_key"])

    def downloadAllFromCloud(self, control=True): #downloads all from the cloud and creats the json files
        if control: #controls if the file is recent (max 1 day old)
            fname = "aggiunte.json"
            if os.path.isfile(fname):
                print("Existing file detected!")
                midnight = datetime.combine(datetime.today(), time.min).timestamp() #in realta segna le 11, ma vabbeh
                if midnight-creation_date(fname) < 0:   #the file was modified today

                    with open('pizze.json') as f:   #reading the json-data from local files
                        self.ElencoPizze = json.load(f)
                        self.ElencoPizze = self.ElencoPizze["record"]
                    with open('ingredienti.json') as f:
                        self.ElencoIngredienti = json.load(f)
                        self.ElencoIngredienti = self.ElencoIngredienti["record"]
                    with open('aggiunte.json') as f:
                        self.ElencoAggiunte = json.load(f)
                        self.ElencoAggiunte = self.ElencoAggiunte["record"]

                else:
                    print("But is too old.")
                    self.downloadAllFromCloud(False)
            else:
                self.downloadAllFromCloud(False)

        else:
            print("Downloading the files from the cloud...")
            self.ElencoPizze = self.c.read(self.data["pizze"])
            self.ElencoIngredienti = self.c.read(self.data["ingredienti"])
            self.ElencoAggiunte = self.c.read(self.data["aggiunte"])

            saveJsonFile("pizze", self.ElencoPizze)
            saveJsonFile("ingredienti", self.ElencoIngredienti)
            saveJsonFile("aggiunte", self.ElencoAggiunte)

            self.ElencoPizze = json.loads(self.ElencoPizze)["record"]
            self.ElencoIngredienti = json.loads(self.ElencoIngredienti)["record"]
            self.ElencoAggiunte = json.loads(self.ElencoAggiunte)["record"]

    def uploadAll(self):
        #uploadda le pizze
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
        self.c.update(dbPizzaList, self.data["pizze"])

        #uploadda gli ingredienti
        queryingredienti = ("""
            SELECT *
            FROM `ingredienti`
        """)
        dbIngredientsList = db.readByQuery(queryingredienti, "json")
        self.c.update(dbIngredientsList, self.data["ingredienti"])
        #uploadda le aggiunte
        queryAggiunte = ("""
            SELECT *
            FROM `aggiunte`
        """)
        dbAggiunteList = db.readByQuery(queryAggiunte, "json")
        self.c.update(dbAggiunteList, self.data["aggiunte"])

    def get_pizzas(self, merge=False):
        if merge:
            elencoEsteso = []
            for i in self.ElencoPizze:  #scorro le pizze
                elencoEsteso.append(i)
                ingredientiScritti = []
                ingredientiScrittiInglese = []
                ingredienti = i["ingredienti"]
                ingredienti = list(ingredienti.split(","))
                for id_ingrediente in ingredienti:  #scorro gli ingredienti della pizza
                    for id_elencoIngrediente in self.ElencoIngredienti: #scorro tutti gli ingredienti
                        if id_elencoIngrediente["id_ingrediente"] == int(id_ingrediente):
                            ingredientiScritti.append(id_elencoIngrediente["nome_italiano"])
                            ingredientiScrittiInglese.append(id_elencoIngrediente["nome_inglese"])
                            
                elencoEsteso[-1]["ingredienti"] = ','.join(ingredientiScritti)
                elencoEsteso[-1]["ingredientiInglese"] = ','.join(ingredientiScrittiInglese)
            return elencoEsteso
        else:
            return self.ElencoPizze

    def get_aggiunte(self):
        return self.ElencoAggiunte

    def get_ingredienti(self):
        return self.ElencoIngredienti

def creation_date(path_to_file):
    return os.path.getmtime(path_to_file)


if __name__ == "__main__":
    """p = Pizzas("jsonBins.json")
    p.downloadAllFromCloud()"""

    #la seguente parte di codice mi servira per uploaddare il menu modificato
    p = Pizzas("jsonBins.json")
    p.uploadAll()
