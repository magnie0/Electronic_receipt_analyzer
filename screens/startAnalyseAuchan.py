from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from queue import Queue
from utils.imageToText import ImagetoText
from auchan.receiptToProduct import Receipt_To_Product
from database.operationsDatabase import DatabaseProducts
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

        self.database = DatabaseProducts('auchan.json')


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

    def check_database(self, instance):
        q = self.database.Check_database_for_products(self.products)
        if not q.empty():
            loadcategories_screen = self.manager.get_screen('LoadCategoriesScreen')
            loadcategories_screen.Update_Values_To_Categorise(q)
            self.manager.current = 'LoadCategoriesScreen'
        else:
            self.SaveResult.disabled = False
            for p in self.products:
                name = p.Get_Name()
                cat0, cat1, cat2 = self.database.Get_categories(name)
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
        for p in self.products:
            page.append(p.To_Array())
        wb.save(filename = workbook_name)
        print("Saved")