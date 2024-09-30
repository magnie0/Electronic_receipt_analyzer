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
        self.ReloadDatabaseButton = Button(text="ReloadDatabase", on_press=self.load_database)
        self.layout.add_widget(self.ReloadDatabaseButton)
        self.AnalyseButton = Button(text="Analyse", on_press=self.switch_to_LoadCategoriesScreen)
        self.AnalyseButton.disabled = True
        self.layout.add_widget(self.AnalyseButton)
        self.add_widget(self.layout)

        self.name_file = 'auchan.json' #TODO change operations regarding database


    def load_file(self, instance):
        input_str = ImagetoText(self.file_name.text)
        date = '2024-09-13'
    
        self.products = Receipt_To_Product(input_str,date)#without set categories
        for p in self.products:
            p.Set_Category('','','')
            print(p.To_Array())

        self.AnalyseButton.disabled = False
        self.LoadFileLabel.text = 'Loaded'

    
    def load_database(self, instance):
        with open('./database/'+self.name_file, 'r') as file:
            self.database = json.load(file)
        print(self.database)

    def flatten_dict(d, parent_key=()):
        items = []
        for k, v in d.items():
            new_key = parent_key + (k,)  # Build the new tuple key
            if isinstance(v, dict):  # If the value is a dictionary, recursively flatten it
                items.extend(flatten_dict(v, new_key).items())
            else:
                items.append((new_key, v))  # Add the new key-value pair
        return dict(items)

    def switch_to_LoadCategoriesScreen(self, instance):
        loadcategories_screen = self.manager.get_screen('LoadCategoriesScreen')
        q = Queue()
        q.put('CYTRYNY')
        q.put('SOK')

        loadcategories_screen.Update_Values_To_Categorise(q)
        
        self.manager.current = 'LoadCategoriesScreen'