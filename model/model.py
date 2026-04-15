from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getYear(self):
        return DAO.getYear()

    def getBrand(self):
        return DAO.getBrand()

    def getRetailers(self):
        return DAO.getRetailers()

    def getTopVendite(self, year, brand, retailer):
        return DAO.getTopVendite(year, brand, retailer)

    def getAnalisiVendite(self, year, brand, retailer):
        return DAO.getAnalisiVendite(year, brand, retailer)