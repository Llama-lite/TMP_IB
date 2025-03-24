from Product import Product
import datetime

class Cup(Product):

    def __init__(self, supplyDate, name, ammount, volume):
        super().__init__(supplyDate, name, ammount)
        self.__volume = volume
    
    @property
    def volume(self):
        return self.__volume
    
    def __str__(self):
        return f'Type: Cup, Date:{self.supplyDate.date()}, Name:{self.name}, Value:{self.ammount}, Volume:{self.volume}'