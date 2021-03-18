from cloud import Cloud
import json
from database import database, list2Json, saveJsonFile

class Pizzas():
    def __init__(self, fname):
        with open(fname) as f:
            self.data = json.load(f)
        self.c = Cloud(self.data["m_key"])

    def downloadAllFromCloud(self): #downloads all from the cloud and creats the json files
        self.ElencoPizze = self.c.read(self.data["pizze"])
        self.ElencoIngredienti = self.c.read(self.data["ingredienti"])
        self.ElencoAggiunte = self.c.read(self.data["aggiunte"])

        saveJsonFile("pizze", self.ElencoPizze)
        saveJsonFile("ingredienti", self.ElencoIngredienti)
        saveJsonFile("aggiunte", self.ElencoAggiunte)

    def uploadAll(self):
        #uploadda le pizze
        db = database("localhost", self.data["dbUserName"], self.data["dbPassword"], self.data["dbData"])
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


if __name__ == "__main__":
    """p = Pizzas("jsonBins.json")
    p.downloadAllFromCloud()"""

    #la seguente parte di codice mi servira per uploaddare il menu modificato
    p = Pizzas("jsonBins.json")
    p.uploadAll()