from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from screens.addProducts import LoadCategoriesScreen
from screens.startAnalyseAuchan import AuchanAnalyseScreen
class MyLayoutSwitchApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(AuchanAnalyseScreen(name='AuchanAnalyseScreen'))
        # Add different layout screens
        sm.add_widget(LoadCategoriesScreen('auchan.json',name='LoadCategoriesScreen'))
        
        return sm

# Run the app
if __name__ == '__main__':
    MyLayoutSwitchApp().run()