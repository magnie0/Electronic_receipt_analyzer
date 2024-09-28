from auchan.receiptToProduct import Receipt_To_Product
def Analyse_Receipt_Auchan(input_str,date):
    #TODO check version of excel categories

    
    products = Receipt_To_Product(input_str,date)#without set categories
    for p in products:
        p.Set_Category('','','')
        print(p.To_Array())

    

