
class Product:
    def __init__(self, date, item, c, quant, price, total):
        self.date = date
        self.item = item
        self.code = c
        self.quant = quant
        self.price = price
        self.total = total

    def __repr__(self):
        return f"Product:{self.item}"

    def Get_Name(self):
        self.item

    def Set_Category(self, kat0, kat1, kat2):
        self.kat0 = kat0
        self.kat1 = kat1
        self.kat2 = kat2
        

    def To_Array(self):
        arr = []
        arr.append(self.date)
        arr.append(self.kat0)
        arr.append(self.kat1)
        arr.append(self.kat2)
        arr.append(self.item)
        arr.append(self.quant)
        arr.append(self.price)
        arr.append(self.total)
        return arr


