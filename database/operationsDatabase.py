import json
from queue import Queue
class DatabaseProducts():
    """
    Class that stores database of products

    Attributes
    ----------
    path_database : str
        path to file with database
    database : dict
        dictionary of categories to receipt loaded from json 
    flatten_database : dict
        converted self.database to (name_on_recipt/part_of_receipt) -> (cat0, cat1, cat2) for faster retrieving information

    Public methods
    -------
    Check_database_for_products(list_of_products)
        Checking if products exist in database if not the names are added to queue
    
    Get_categories(name_on_receipt)
        Gets categories of product, function return a tuple (cat0, cat1, cat2)
    
    """
    #database_file_name is the name of the shop for example auchan.json
    def __init__(self, database_file_name): #TODO delete database_file_name olf self.file_name
        self.path_database = './database/'+database_file_name 
        self.database = dict() #loaded from json 
        self.flatten_database = dict() #converted self.database to (name_on_recipt/part_of_receipt) -> (cat0, cat1, cat2) 
        self.reload_database()

    def reload_database(self):
        """Reloads database from file specified when creating object"""
        with open(self.path_database, 'r') as file:
            self.database = json.load(file)
        self.flatten_dict()

    #flatten database from 
    def flatten_dict(self):
        self.flatten_database = dict()
        for cat0, v0 in self.database.items():
            for cat1, v1 in v0.items():
                for cat2, v2 in v1.items():
                    for element in v2:
                        triplet = (cat0, cat1, cat2)
                        self.flatten_database[element] = triplet

    #part of receipt can identify a product
    def part_identifies_product(self, name):
        for part in name.split():
            if part in self.flatten_database:
                return True 
        return False
    
    def Get_categories(self, name): 
        if name in self.flatten_database:
            return self.flatten_database[name]
        for part in name.split():
            if part in self.flatten_database:
                return self.flatten_database[part]
        

    def Check_database_for_products(self, products):
        self.reload_database()
        q = Queue()
        for p in products:
            name = p.Get_Name()
            if name not in self.flatten_database and not self.part_identifies_product(name):
                q.put(name)
        return q
    
    def Get_database(self):
        return self.database
    
    def Save_database(self):
        json_object = json.dumps(self.database, ensure_ascii=False, indent=4).encode('utf8')
        with open(self.path_database, 'w') as file:
            file.write(json_object.decode())
