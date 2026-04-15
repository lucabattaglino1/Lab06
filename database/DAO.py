from database.DB_connect import DBConnect
from model.go_retailers import Go_retailers


class DAO():
    def __init__(self):
        pass

    # questa è la prima query al database per prendere tutti gli anni
    @staticmethod
    def getYear():
        cnx = DBConnect.get_connection() #connessione
        cursor = cnx.cursor(dictionary=True) #creo cursore

        # query scritta su DBVEAR
        query = """SELECT YEAR(date) AS year
                    FROM go_daily_sales
                    ORDER BY year"""

        cursor.execute(query) #eseguo la query

        # ciclo su cursore per leggere i dati
        # li inserisco in una lista
        res = []
        for row in cursor:
            res.append(row["year"])


        cursor.close() # chiudo cursore
        cnx.close() # restituisco connessione
        return res # return della lista


    @staticmethod
    def getBrand():
        cnx = DBConnect.get_connection()  # connessione
        cursor = cnx.cursor(dictionary=True)  # creo cursore

        # query scritta su DBVEAR
        query = """SELECT product_brand
                    FROM go_products
                    ORDER BY product_brand"""

        cursor.execute(query)  # eseguo la query

        # ciclo su cursore per leggere i dati
        # li inserisco in una lista
        res = []
        for row in cursor:
            res.append(row["product_brand"])

        cursor.close()  # chiudo cursore
        cnx.close()  # restituisco connessione
        return res  # return della lista

    # per popolare il dropdown retailer
    @staticmethod
    def getRetailers():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        # con l'asterisco leggo tutto
        query = """SELECT retailer_code, retailer_name, type, country
                    FROM go_retailers
                    ORDER BY retailer_name"""

        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Go_retailers(
                retailer_code=row["retailer_code"],
                retailer_name=row["retailer_name"],
                type=row["type"],
                country=row["country"]
            ))

        cursor.close()
        cnx.close()
        return res

    # PUNTO 2
    @staticmethod
    def getTopVendite(year, brand, retailer): #questo metodo riceve year, brand, retailer
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        # cosa fala query?
        # mi serve data, brand e retailer e ricavo calcolato
        # from le tre tabelle e join tra le tabelle
        query = """
            SELECT gds.date, gp.product_brand, gr.retailer_name,
                   gds.unit_sale_price * gds.quantity AS ricavo
            FROM go_daily_sales gds, go_products gp, go_retailers gr
            WHERE gds.product_number = gp.product_number
            AND gds.retailer_code = gr.retailer_code
        """

        # aggiungo filtri SOLO se selezionati

        # se l'utente ha scelto un anno aggiungo il filtro alla query
        if year is not None:
            query += f" AND YEAR(gds.date) = {year}"

        # se l'utente ha scelto un brand aggiungo il filtro alla query
        if brand is not None:
            query += f" AND gp.product_brand = '{brand}'"

        # se l'utente ha scelto un retailer aggiungo il filtro alla query
        if retailer is not None:
            query += f" AND gr.retailer_code = {retailer}"

        # ordino per ricavo
        # come mi dice la consegna --> prendi solo i primi 5
        query += """
            ORDER BY ricavo DESC
            LIMIT 5
        """

        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res


    # PUNTO 3
    # obiettivo:
    # calcolare totale ricavi, numero vendite, numero retailer diversi, numero prodotti diversi
    @staticmethod
    def getAnalisiVendite(year, brand, retailer):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        # spiegazione query
        # nella prima riga ho la somma di tutti i ricavi (giro d'affari)
        # nella seconda conto tutte le righe così ho il numero di vendite
        # nella terza conto il numero di retailer (senza duplicati --> distinct)
        # nella quarta conto i prodotti diversi
        # from delle tabelle che mi servono e doppio join perchè ho 3 tabelle
        query = """
            SELECT 
                SUM(gds.unit_sale_price * gds.quantity) AS totale,
                COUNT(*) AS num_vendite,
                COUNT(DISTINCT gds.retailer_code) AS num_retailer,
                COUNT(DISTINCT gds.product_number) AS num_prodotti
            FROM go_daily_sales gds, go_products gp, go_retailers gr
            WHERE gds.product_number = gp.product_number
            AND gds.retailer_code = gr.retailer_code
        """

        # qui aggiungo i filtri solo se serve --> come nel punto 2
        if year is not None:
            query += f" AND YEAR(gds.date) = {year}"

        if brand is not None:
            query += f" AND gp.product_brand = '{brand}'"

        if retailer is not None:
            query += f" AND gr.retailer_code = {retailer}"

        cursor.execute(query)

        # per ottenere una singola riga
        # generalmente si usa fetchone quando ho aggregazioni (sum,count,avg)
        result = cursor.fetchone()

        cursor.close()
        cnx.close()

        return result