import mysql.connector
from mysql.connector import Error
import json
from libraries.utils.logger import Logger

class database():

    _log_file: str
    connectionTracker = True #remouves spam comments

    def __init__(self, host, user, password, database, restaurant_name=""):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self._logger = Logger()

        self.con = self.connect()
        self.restaurant_name = restaurant_name
        if self.con != None:
            self._logger.disp("Connected")
            self.con.close()
        else:
            self.connectionTracker = False
            self._logger.disp("Can't connect to database. Default language will be used")

    def readByQuery(self, query, form=None):
        self.con = self.connect()
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
        self.con = self.connect()
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
        self.con = self.connect()
        cursor = self.con.cursor()
        query = ("""
            SELECT nome_aggiunta, nome_inglese, prezzo_aggiunta
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
                self._logger.disp("Error while connecting to MySQL", e)

    def getCurrentLanguage(self):
        try:
            if self.restaurant_name != "":
                self.con = self.connect()
                cursor = self.con.cursor(buffered=True)
                query = f"""
                    SELECT language_name
                    FROM `restaurants`
                    INNER JOIN languages ON restaurants.id_language = languages.id
                    WHERE restaurants.restaurant_name = '{self.restaurant_name}';
                    """
                cursor.execute(query)
                self.con.close()
                return cursor.fetchone()[0]
            else:
                return "nome_italiano"
        except:
            return "nome_italiano"

def list2Json(table, columns):  #translates a matrix into a json
    keys = [i[0] for i in columns]
    dictionary = []
    for line in table:
        dictionary.append(dict(zip(keys, line)))
    return dictionary

def saveJsonFile(fileName, jsonObj):
    with open(fileName, 'w') as f:
        f.write(jsonObj)

if __name__ == "__main__":
    with open("DBsetup.json") as f:
        data = json.load(f)
    db = database("localhost", data["dbUserName"], data["dbPassword"], data["dbData2BeUploaded"])
    data = db.  read_data()
    for i in data:
        print(i, "\n")
