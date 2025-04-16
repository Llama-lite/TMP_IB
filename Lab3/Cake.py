from Product import Product
from datetime import datetime

class Cake(Product):
    """Represents a cake product with height attribute"""

    def __init__(self, supplyDate: datetime, name: str, amount: int, height: int):
        """
        Initialize a Cake product
        
        Args:
            supplyDate (datetime): Date when the cakes will be supplied
            name (str): Name of the cakes
            ammount (int): Amount of the cakes
            height (int): Height of the cakes
        """
        super().__init__(supplyDate, name, amount)
        self.__height = height
    
    @property
    def height(self) -> int:
        """Get the cake height"""
        return self.__height
    
    def __str__(self) -> str:
        """String representation of the cake"""
        return f'Cake({self.supplyDate.date().strftime("%d.%m.%Y")}, \"{self.name}\", {self.amount}, {self.height})'