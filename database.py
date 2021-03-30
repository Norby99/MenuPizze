import mysql.connector
from mysql.connector import Error
import json
import datetime

class database():
    connectionTracker = True #remouves spam comments

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.con = self.connect()
        if self.con != None:
            print("Connected")
            self.con.close()
        else:
            self.connectionTracker = False
            print("Can't connect to database. Default language will be used")

    def readByQuery(self, query, form=None):
        cursor = self.con.cursor(buffered=True)
        cursor.execute(query)
        table = cursor.fetchall()
        self.con.close()
        if form == "json":  #retruns the table as a json
            dictionary = list2Json(table, cursor.description)
            
            #json_object = json.dumps(dictionary, indent = 4)
            return dictionary
        return table

    def read_data(self, form=None):
        cursor = self.con.cursor(buffered=True)
        query = "SELECT lingua from lingue"
        cursor.execute(query)
        lingua = cursor.fetchone()[0]

        cursor = self.con.cursor()
        query = ("""
            SELECT pizze.id, nomePizza, nome_tipo, prezzo, GROUP_CONCAT(""" + lingua + """ ORDER BY `pizza-ingredienti`.`id_collegamento`) AS "ingredienti"
            FROM pizze
            INNER JOIN tipo_pizze ON tipo_pizze.id_tipo = pizze.id_tipo
            INNER JOIN `pizza-ingredienti` ON pizze.id = `pizza-ingredienti`.id_pizza
            INNER JOIN ingredienti ON ingredienti.id_ingrediente = `pizza-ingredienti`.`id_ingrediente`
            GROUP BY nomePizza
            ORDER BY pizze.id
        """)
        cursor.execute(query)
        table = cursor.fetchall()
        self.con.close()

        if form == "json":  #retruns the table as a json
            dictionary = list2Json(table, cursor.description)
            
            json_object = json.dumps(dictionary, indent = 4)
            return json_object
        
        return table

    def read_aggiunte(self):
        cursor = self.con.cursor()
        query = ("""
            SELECT nome_aggiunta, prezzo_aggiunta
            FROM aggiunte
            ORDER BY id_aggiunta
        """)
        cursor.execute(query)
        result = cursor.fetchall()
        self.con.close()
        return result
        

    def connect(self):
        try:
            connection = mysql.connector.connect(
                                                host=self.host,
                                                user=self.user,
                                                password=self.password,
                                                database=self.database,
                                                buffered=True)
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("select database()")
                self.connectionTracker = True
                return connection

        except Error as e:
            if self.connectionTracker:
                self.connectionTracker = False
                print("Error while connecting to MySQL", e)

    def getCurrentLanguage(self):
        try:
            self.con = self.connect()
            cursor = self.con.cursor(buffered=True)
            query = """SELECT *
                    FROM `lingua`"""
            cursor.execute(query)
            self.con.close()
            return cursor.fetchone()[1]
        except:
            return "nome_italiano"

def list2Json(table, columns):  #translates a matrix into a json
    keys = [i[0] for i in columns]
    dictionary = []
    for line in table:
        dictionary.append(dict(zip(keys, line)))
    return dictionary

def saveJsonFile(fileName, jsonObj):
        with open(fileName+'.json', 'w') as f:
            f.write(jsonObj)

if __name__ == "__main__":
    db = database("localhost", "MirkoFagnocchi", "margherita1", "menu_pizzeria")
    data = db.read_data()
    for i in data:
        print(i, "\n")

