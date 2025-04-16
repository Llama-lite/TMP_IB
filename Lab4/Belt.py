from Product import Product
from datetime import datetime

class Belt(Product):
    """Represents a belt product with metal/non-metal attribute"""
    
    def __init__(self, supplyDate: datetime, name: str, amount: int, metal: bool):
        """
        Initialize a Belt product
        
        Args:
            supplyDate (datetime): Date when the belts will be supplied
            name (str): Name of the belts
            ammount (int): Amount of the belts
            metal (bool): Whether the belts is made of metal
        """
        super().__init__(supplyDate, name, amount)
        self.__metal = metal
    
    @property
    def metal(self) -> bool:
        """Get whether the belt is made of metal"""
        return self.__metal
    
    def __str__(self) -> str:
        """String representation of the belt"""
        return f'Belt({self.supplyDate.date().strftime("%d.%m.%Y")}, \"{self.name}\", {self.amount}, {self.metal})'