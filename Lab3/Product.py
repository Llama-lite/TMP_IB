from datetime import datetime

class Product:
    """Base class for all product types"""
    
    def __init__(self, supplyDate, name, amount):
        """Initialize a Product
        
        Args:
            supplyDate (datetime): Date when product will be supplied
            name (str): Name of the product
            amount (int): Amount of the product
        """
        self.__supplyDate = supplyDate
        self.__name = name
        self.__amount = amount
    
    @property
    def name(self) -> str:
        """Get the product name"""
        return self.__name

    @property
    def supplyDate(self) -> datetime:
        """Get the product supplyDate"""
        return self.__supplyDate

    @property
    def amount(self) -> int:
        """Get the product amount"""
        return self.__amount

    def __str__(self) -> str:
        """String representation of the product (Should be implemented by subclasses)"""
        raise NotImplementedError()
