from GoodsSupply import GoodsSupply
import datetime

class Belt(GoodsSupply):

    def __init__(self, supplyDate, name, ammount, metal):
        super().__init__(self, supplyDate, name, ammount)
        self.__metal = metal
    
    @property
    def metal(self):
        return self.__metal
    
    def read(self, message):
        values = message.split(',')
        self,supplyDate = datetime.datetime.strptime(message[0], '%Y.%m.%d')
        self.name = message[1]
        self.ammount = int(message[2])
        self.metal = bool(message[3])
    
    def __str__(self):
        print(f'Type: Belt, Date:{self.supplyDate.date()}, Name:{self.name}, Value:{self.value}, Metal?:{self.metal}')