from Product import Product

class Cup(Product):

    def __init__(self, supplyDate, name, ammount, volume):
        super().__init__(supplyDate, name, ammount)
        self.__volume = volume
    
    @property
    def volume(self):
        return self.__volume
    
    def __str__(self):
        return f'Cup({self.supplyDate.date().strftime("%d.%m.%Y")}, \"{self.name}\", {self.ammount}, {self.volume})'