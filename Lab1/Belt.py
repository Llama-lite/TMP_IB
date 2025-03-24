from Product import Product
import datetime

class Belt(Product):

    def __init__(self, supplyDate, name, ammount, metal):
        super().__init__(supplyDate, name, ammount)
        self.__metal = metal
    
    @property
    def metal(self):
        return self.__metal
    
    def __str__(self):
        return f'Type: Belt, Date:{self.supplyDate.date()}, Name:{self.name}, Value:{self.ammount}, Metal?:{self.metal}'