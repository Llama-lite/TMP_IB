from Product import Product

class Cake(Product):

    def __init__(self, supplyDate, name, ammount, height):
        super().__init__(supplyDate, name, ammount)
        self.__height = height
    
    @property
    def height(self):
        return self.__height
    
    def __str__(self):
        return f'Cake({self.supplyDate.date().strftime("%d.%m.%Y")}, \"{self.name}\", {self.ammount}, {self.height})'