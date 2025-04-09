from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYear():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year (g.Date) anno
                        from go_daily_sales g 
                        order by anno desc
                                   """
        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNazioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r.Country
                    from go_retailers r
                    order by r.Country asc
                                   """
        cursor.execute(query)

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def getNodes(nazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from go_retailers r
                    where r.Country =%s
                                           """
        cursor.execute(query, (nazione,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getEdges(nazione,anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.Retailer_code ret1, r2.Retailer_code ret2, count(distinct s1.Product_number) P
                    from go_retailers r1, go_retailers r2, go_daily_sales s1, go_daily_sales s2
                    where r1.Retailer_code <r2.Retailer_code
                    and r1.Retailer_code =s1.Retailer_code
                    and r2.Retailer_code =s2.Retailer_code
                    and s1.Product_number =s2.Product_number
                    and r1.Country =r2.Country
                    and r1.Country =%s
                    and year(s1.Date)=year(s2.Date)
                    and year(s1.Date)=%s
                    group by r1.Retailer_code, r2.Retailer_code
                    order by r1.Retailer_code, r2.Retailer_code
                        """
        cursor.execute(query, (nazione,anno))

        for row in cursor:
            result.append((row["ret1"], row["ret2"], row["P"]))

        cursor.close()
        conn.close()
        return result
