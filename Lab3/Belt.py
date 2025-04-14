from Product import Product

class Belt(Product):

    def __init__(self, supplyDate, name, ammount, metal):
        super().__init__(supplyDate, name, ammount)
        self.__metal = metal
    
    @property
    def metal(self):
        return self.__metal
    
    def __str__(self):
        return f'Belt({self.supplyDate.date().strftime("%d.%m.%Y")}, \"{self.name}\", {self.ammount}, {self.metal})'