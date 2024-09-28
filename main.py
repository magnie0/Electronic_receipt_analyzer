import sys
from utils.imageToText import ImagetoText
from auchan.analyseReceipt import Analyse_Receipt_Auchan

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
#TODO help if no argument passed
#ex. usage python3 imageToText.py <filename>
filename = sys.argv[1]
#Auchan
# str = ImagetoText(filename)
# Analyse_Receipt_Auchan(str,'2024-09-13')

from excel_categorize.excel import LoadCategoriesScreen
class MyLayoutSwitchApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()

        # Add different layout screens
        sm.add_widget(LoadCategoriesScreen('./excel_categorize/Rozpisanie zakupów .xlsx','Pogląd Mappingu',name='CreateCategories'))
#categories = LoadCategories('./excel_categorize/Rozpisanie zakupów .xlsx','Pogląd Mappingu')

        return sm

# Run the app
if __name__ == '__main__':
    MyLayoutSwitchApp().run()