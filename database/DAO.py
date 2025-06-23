from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(row["id_fermata"],
                                  row["nome"],
                                  row["coordX"],
                                  row["coordY"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasConnessione(nodo_01: Fermata, nodo_02: Fermata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query="""SELECT *
        FROM connessione c
        WHERE c.id_stazP = %s AND c.id_stazA = %s"""
        cursor.execute(query, (nodo_01.id_fermata, nodo_02.id_fermata))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result)>0

    @staticmethod
    def getVicini(nodo_01: Fermata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
            FROM connessione c
            WHERE c.id_stazP = %s"""
        cursor.execute(query, (nodo_01.id_fermata,))
        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT *
                FROM connessione c"""
        cursor.execute(query,)
        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesPesati():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT id_stazP, id_stazA, COUNT(*) AS n
        FROM connessione c
        GROUP BY id_stazP, id_stazA"""
        cursor.execute(query, )
        for row in cursor:
            result.append((row["id_stazP"], row["id_stazA"], row["n"])) # --> sono tuple
        cursor.close()
        conn.close()
        return result