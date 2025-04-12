class Product:

    def __init__(self, supplyDate, name, ammount):
        self.__supplyDate = supplyDate
        self.__name = name
        self.__ammount = ammount
    
    @property
    def date(self):
        return self.__name
    
    @property
    def name(self):
        return self.__name

    @property
    def supplyDate(self):
        return self.__supplyDate

    @property
    def ammount(self):
        return self.__ammount

    def __str__(self):
        raise NotImplementedError()
