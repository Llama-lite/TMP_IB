from Product import Product
from datetime import datetime

class Cup(Product):
    """Represents a cup product with volume attribute"""

    def __init__(self, supplyDate: datetime, name: str, amount: int, volume: int):
        """
        Initialize a Cup product
        
        Args:
            supplyDate (datetime): Date when the cups will be supplied
            name (str): Name of the cups
            ammount (int): Amount of the cups
            volume (int): Volume of the cups
        """
        super().__init__(supplyDate, name, amount)
        self.__volume = volume
    
    @property
    def volume(self) -> int:
        """Get the cup volume"""
        return self.__volume
    
    def __str__(self) -> str:
        """String representation of the cup"""
        return f'Cup({self.supplyDate.date().strftime("%d.%m.%Y")}, \"{self.name}\", {self.amount}, {self.volume})'