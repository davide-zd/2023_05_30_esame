from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    # metodo per prendere gli anni (dal 2015 al 2018) dal database
    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(year(gds.`Date`)) anno
                    from go_daily_sales gds"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])
        cursor.close()
        conn.close()
        return result

    # metodo per prendere le nazioni dal database
    @staticmethod
    def getNazioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(gr.Country) nazione
                    from go_retailers gr 
                    order by Country"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["nazione"])
        cursor.close()
        conn.close()
        return result

    # metodo per prendere i nodi
    @staticmethod
    def getNodes(nazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gr.Retailer_code id, gr.Retailer_name nome
                    from go_retailers gr 
                    where gr.Country = %s
                    order by gr.Retailer_name"""
        cursor.execute(query, (nazione,))

        for row in cursor:
            result.append(Retailer(**row))
        cursor.close()
        conn.close()
        return result

    # metodo per prendere gli archi
    @staticmethod
    def getEdges(nazione, numero, anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """select r1.Retailer_code n1, r2.Retailer_code n2, COUNT(distinct(s1.Product_number)) peso
                    from go_daily_sales s1, go_daily_sales s2, go_retailers r1, go_retailers r2
                    where year(s1.`Date`) = %s
                        and year(s1.`Date`) = year(s2.`Date`)
                        and s1.Product_number = s2.Product_number
                        and s1.Retailer_code = r1.Retailer_code
                        and s2.Retailer_code = r2.Retailer_code
                        and r1.Country = %s 
                        and r1.Country = r2.Country
                        and r1.Retailer_code < r2.Retailer_code
                    group by n1, n2
                    having peso >= %s"""
        cursor.execute(query, (anno, nazione, numero))

        for row in cursor:
            result.append((row["n1"], row["n2"], row["peso"]))
        cursor.close()
        conn.close()
        return result
