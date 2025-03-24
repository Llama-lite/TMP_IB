import datetime

class GoodsSupply:

    def __init__(self, name, supplyDate, ammount):
        self.__name = name
        self.__supplyDate = supplyDate
        self.__ammount = ammount
    
    @property
    def name(self):
        return self.__name

    @property
    def supplyDate(self):
        return self.__supplyDate

    @property
    def ammount(self):
        return self.__ammount

    def read(self, message):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()
