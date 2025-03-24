from GoodsSupply import GoodsSupply
import datetime

class Cup(GoodsSupply):

    def __init__(self, supplyDate, name, ammount, volume):
        super().__init__(self, supplyDate, name, ammount)
        self.__volume = volume
    
    @property
    def volume(self):
        return self.__volume
    
    def read(self, message):
        values = message.split(',')
        self,supplyDate = datetime.datetime.strptime(message[0], '%Y.%m.%d')
        self.name = message[1]
        self.ammount = int(message[2])
        self.volume = int(message[3])
    
    def __str__(self):
        print(f'Type: Cup, Date:{self.supplyDate.date()}, Name:{self.name}, Value:{self.value}, Volume:{self.volume}')