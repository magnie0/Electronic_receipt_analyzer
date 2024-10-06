from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from queue import Queue
from utils.imageToText import ImagetoText
from auchan.receiptToProduct import Receipt_To_Product
import json
class AuchanAnalyseScreen(Screen):
    def __init__(self, **kwargs):
        super(AuchanAnalyseScreen, self).__init__(**kwargs)
        
        # Create BoxLayout and add buttons
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.file_name = TextInput(text='2024-09-13.jpg', multiline=False)
        self.layout.add_widget(self.file_name)
        self.file_name.bind(text = self.change_input_file_listener)

        LoadLayout = BoxLayout(orientation='horizontal', spacing=10)
        self.LoadFileButton = Button(text="LoadFile", on_press=self.load_file)
        self.LoadFileLabel = Label(text='Not loaded')
        LoadLayout.add_widget(self.LoadFileButton)
        LoadLayout.add_widget(self.LoadFileLabel)
        self.layout.add_widget(LoadLayout)

        self.ReloadDatabaseButton = Button(text="ReloadDatabase", on_press=self.check_database)
        self.layout.add_widget(self.ReloadDatabaseButton)
        self.ReloadDatabaseButton.disabled = True

        self.SaveResult = Button(text="SaveResult", on_press=self.saveResult)
        self.layout.add_widget(self.SaveResult)
        self.SaveResult.disabled = True
        
        self.add_widget(self.layout)

        self.name_file = 'auchan.json' #TODO change operations regarding database

    def change_input_file_listener(self, instane, text):
        self.LoadFileLabel.text = 'Not loaded'
        self.ReloadDatabaseButton.disabled = True
        self.SaveResult.disabled = True

    def load_file(self, instance):
        input_str = ImagetoText(self.file_name.text)
        last_dot_index = self.file_name.text.rfind('.')
        self.date = '1970-01-01'
        if last_dot_index != -1:
            self.date = self.file_name.text[:last_dot_index]
        self.products = Receipt_To_Product(input_str,self.date )#without set categories
        self.ReloadDatabaseButton.disabled = False
        self.LoadFileLabel.text = 'Loaded'

    
    def load_database(self):
        with open('./database/'+self.name_file, 'r') as file:
            self.database = json.load(file)
        self.flatten_dict()

    def flatten_dict(self):
        self.flatten_database = dict()
        for cat0, v0 in self.database.items():
            for cat1, v1 in v0.items():
                for cat2, v2 in v1.items():
                    for element in v2:
                        triplet = (cat0, cat1, cat2)
                        self.flatten_database[element] = triplet

    def part_identifies_product(self, name):
        for part in name.split():
            if part in self.flatten_database:
                return True 
        return False
    
    def get_triple(self, name):
        if name in self.flatten_database:
            return self.flatten_database[name]
        for part in name.split():
            if part in self.flatten_database:
                return self.flatten_database[part]
        

    def check_database(self, instance):
        self.load_database()
        loadcategories_screen = self.manager.get_screen('LoadCategoriesScreen')
        q = Queue()
        for p in self.products:
            name = p.Get_Name()
            if name not in self.flatten_database and not self.part_identifies_product(name):
                q.put(name)


        if not q.empty():
            loadcategories_screen.Update_Values_To_Categorise(q)
            self.manager.current = 'LoadCategoriesScreen'
        else:
            self.SaveResult.disabled = False
            for p in self.products:
                name = p.Get_Name()
                cat0, cat1, cat2 = self.get_triple(name)
                p.Set_Category(cat0, cat1, cat2)
                print(p.To_Array())




    def saveResult(self, instance):
        print("Saving")
        from openpyxl.workbook import Workbook
        workbook_name = self.date+".xlsx"
        wb = Workbook()
        page = wb.active
        page.title = 'events'
        workbook = Workbook()
        headers = ['date','cat0','cat1','cat2','name_on_receipt','quant','price','total']
        page.append(headers) # write the headers to the first line
        #data = [['description1','date1','time1','location1','latitude1','longitude1']]
        for p in self.products:
            page.append(p.To_Array())
        wb.save(filename = workbook_name)