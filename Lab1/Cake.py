from GoodsSupply import GoodsSupply
import datetime

class Cake(GoodsSupply):

    def __init__(self, supplyDate, name, ammount, height):
        super().__init__(self, supplyDate, name, ammount)
        self.__height = height
    
    @property
    def height(self):
        return self.__height
    
    def read(self, message):
        values = message.split(',')
        self,supplyDate = datetime.datetime.strptime(message[0], '%Y.%m.%d')
        self.name = message[1]
        self.ammount = int(message[2])
        self.height = float(message[3])
    
    def __str__(self):
        print(f'Type: Cake, Date:{self.supplyDate.date()}, Name:{self.name}, Value:{self.value}, Height:{self.height}')