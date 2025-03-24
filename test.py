from GoodsSupply import GoodsSupply
from Cake import Cake
from Cup import Cup
from Belt import Belt



with open("test.txt", "r") as file:
    for line in file:
        supplyType, values = line.split('(').strip()
        values = values[:-1]
        
        print(supplyType)
    # for line in file:
        # swt


