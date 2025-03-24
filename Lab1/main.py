from Cake import Cake
from Cup import Cup
from Belt import Belt
import datetime

def file_to_products_list(filename):
    products = []
    
    with open("supply", "r") as file:
        for line in file:
            supply_type, values = line.strip().split("(")
            values = values[0:-1].split(", ")
            
            if supply_type == "Belt":
                products.append(Belt(supplyDate=datetime.datetime.strptime(values[0], "%d.%m.%Y"), name=values[1][1:-1], ammount=int(values[2]), metal=(values[3].lower() == "true")))
            
            elif supply_type == "Cake":
                products.append(Cake(supplyDate=datetime.datetime.strptime(values[0], "%d.%m.%Y"), name=values[1][1:-1], ammount=int(values[2]), height=int(values[3])))
            
            elif supply_type == "Cup":
                products.append(Cup(supplyDate=datetime.datetime.strptime(values[0], "%d.%m.%Y"), name=values[1][1:-1], ammount=int(values[2]), volume=int(values[3])))
    
    return products

if __name__ == "__main__":
    products = file_to_products_list('supply')
    for product in products:
        print(product)