import pandas as pd
import json
#from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from database.operationsDatabase import DatabaseProducts
class LoadCategoriesScreen(Screen):
    def __init__(self, name_file, **kwargs):
        super(LoadCategoriesScreen, self).__init__(**kwargs)
        self.database = DatabaseProducts(name_file)
        self.layout_page = BoxLayout(orientation='vertical')
        self.create_layout()
        self.add_widget(self.layout_page)
        self.new_products = []
        # Run the app with the layout containing both spinners
        #runTouchApp(self.layout_page)
        
    def create_layout(self):
        # Create a BoxLayout to hold both spinners
        #self.layout_products = BoxLayout(orientation='horizontal', spacing=10,size_hint=(1, .7),pos_hint={'top': 1})
        layout_products = BoxLayout(orientation='horizontal', spacing=10)
        # First Spinner (main category)
 
        tempDatabase = self.database.Get_database()

        cat0 = sorted(list(tempDatabase.keys()))
        current_cat0 = cat0[0]
        self.spinner0 = Spinner(
            text=current_cat0,
            values=cat0,
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'top': 1})

        cat1 = sorted(list(tempDatabase[current_cat0].keys()))
        current_cat1 = cat1[0]
        # Second Spinner (dependent on first spinner's value)
        self.spinner1 = Spinner(
            text=current_cat1,
            values=cat1,
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'top': 1})
        
        cat2 = sorted(list(tempDatabase[current_cat0][current_cat1].keys()))
        current_cat2 = cat2[0]
        self.spinner2 = Spinner(
            text=current_cat2,
            values=cat2,
            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'top': 1})

        def update_spinner1(spinner, text):
            cat1 = sorted(tempDatabase[text].keys())
            self.spinner1.values = cat1
            # Reset the second spinner text when first spinner changes
            self.spinner1.text = self.spinner1.values[0]
        def update_spinner2(spinner, text):
            cat0 = self.spinner0.text
            cat2 = sorted(tempDatabase[cat0][text].keys())
            self.spinner2.values = cat2
            # Reset the second spinner text when first spinner changes
            self.spinner2.text = self.spinner2.values[0]

        # Bind the first spinner to update the second spinner based on selection
        self.spinner0.bind(text=update_spinner1)
        self.spinner1.bind(text=update_spinner2)

        # Add both spinners to the layout
        layout_products.add_widget(self.spinner0)
        layout_products.add_widget(self.spinner1)
        layout_products.add_widget(self.spinner2)

        info = BoxLayout(orientation='vertical',size_hint=(1, 0.5))
        l1 = Label(text='Nie rozpoznany produkt!')
        l2 = Label(text='Wpisz z paragonu całość lub część która pozwala zinterpretować produkt: ')
        self.on_receipt = Label(text='temp')
        receipt_text = TextInput(text='temp', multiline=False)
        info.add_widget(l1)
        info.add_widget(l2)
        info.add_widget(self.on_receipt)
        info.add_widget(receipt_text)
        self.receipt_text = receipt_text
        self.layout_page.add_widget(info)

        self.layout_page.add_widget(layout_products)
        buttons = BoxLayout(orientation='horizontal')
        button1 = Button(text='Dodaj',size=(200, 44),size_hint=(None, None))
        button1.bind(on_press=self.callback)
        button2 = Button(text='Ignore',size=(200, 44),size_hint=(None, None))
        button2.bind(on_press=self.ignore)
        button3 = Button(text='Quit',size=(200, 44),size_hint=(None, None))
        button3.bind(on_press=self.quitAdding)

        buttons.add_widget(button1)
        buttons.add_widget(button2)
        buttons.add_widget(button3)

        self.layout_page.add_widget(buttons)
    def callback(self, instance):
        print(f"The button pressed {self.spinner0.text} {self.spinner1.text} {self.spinner2.text}")
        triplet = (self.spinner0.text, self.spinner1.text, self.spinner2.text)
        print(f"triplet: {triplet}")
        self.database.Get_database()[self.spinner0.text][self.spinner1.text][self.spinner2.text].append(self.receipt_text.text)
        self.handle_next_product()

    def ignore(self,instance):
        self.handle_next_product()
    def quitAdding(self, instance):
        self.database.Save_database()
        self.manager.current = 'AuchanAnalyseScreen'

    def handle_next_product(self):
        if self.new_products.empty():
            self.database.Save_database()
            self.manager.current = 'AuchanAnalyseScreen'
        else:
            self.receipt_text.text = self.new_products.get()
            self.on_receipt.text = self.receipt_text.text

    def Update_Values_To_Categorise(self, new_products):
        self.new_products = new_products
        if self.new_products: #check if empty
            self.receipt_text.text = self.new_products.get()
            self.on_receipt.text = self.receipt_text.text




#categories = LoadCategories('./excel_categorize/Rozpisanie zakupów .xlsx','Pogląd Mappingu')

