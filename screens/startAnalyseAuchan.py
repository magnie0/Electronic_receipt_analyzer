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
        LoadLayout = BoxLayout(orientation='horizontal', spacing=10)
        self.LoadFileButton = Button(text="LoadFile", on_press=self.load_file)
        self.LoadFileLabel = Label(text='Not loaded')
        LoadLayout.add_widget(self.LoadFileButton)
        LoadLayout.add_widget(self.LoadFileLabel)
        self.layout.add_widget(LoadLayout)
        self.ReloadDatabaseButton = Button(text="ReloadDatabase", on_press=self.check_database)
        self.layout.add_widget(self.ReloadDatabaseButton)
        self.SaveResult = Button(text="SaveResult", on_press=self.saveResult)
        self.ReloadDatabaseButton.disabled = True
        self.SaveResult.disabled = True
        self.layout.add_widget(self.SaveResult)
        self.add_widget(self.layout)

        self.name_file = 'auchan.json' #TODO change operations regarding database


    def load_file(self, instance):
        input_str = ImagetoText(self.file_name.text)
        date = '2024-09-13'
    
        self.products = Receipt_To_Product(input_str,date)#without set categories
        self.ReloadDatabaseButton.disabled = False
        self.LoadFileLabel.text = 'Loaded'

    
    def load_database(self):
        with open('./database/'+self.name_file, 'r') as file:
            self.database = json.load(file)
        print(self.database)
        print('========================')
        self.flatten_dict()

    def flatten_dict(self):
        self.flatten_database = dict()
        for cat0, v0 in self.database.items():
            for cat1, v1 in v0.items():
                for cat2, v2 in v1.items():
                    for element in v2:
                        triplet = (cat0, cat1, cat2)
                        self.flatten_database[element] = triplet
        print(self.flatten_database)

    def part_identifies_product(self, name):
        for part in name.split():
            if part in self.flatten_database:
                return True 
        return False

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
            self.AnalyseButton.disabled = False



    def saveResult(self, instance):
        print("Here will be saving")