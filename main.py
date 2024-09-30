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

from screens.excel import LoadCategoriesScreen
from screens.startAnalyseAuchan import AuchanAnalyseScreen
class MyLayoutSwitchApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(AuchanAnalyseScreen(name='AuchanAnalyseScreen'))
        # Add different layout screens
        sm.add_widget(LoadCategoriesScreen('./data/Rozpisanie zakupów .xlsx','Pogląd Mappingu',name='LoadCategoriesScreen'))
        
        return sm

# Run the app
if __name__ == '__main__':
    MyLayoutSwitchApp().run()