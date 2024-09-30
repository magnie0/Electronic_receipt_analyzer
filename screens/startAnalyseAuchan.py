from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from queue import Queue
class AuchanAnalyseScreen(Screen):
    def __init__(self, **kwargs):
        super(AuchanAnalyseScreen, self).__init__(**kwargs)
        
        # Create BoxLayout and add buttons
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.layout.add_widget(Button(text="Analyse", on_press=self.switch_to_LoadCategoriesScreen))
        self.add_widget(self.layout)

    def switch_to_LoadCategoriesScreen(self, instance):
        loadcategories_screen = self.manager.get_screen('LoadCategoriesScreen')
        q = Queue()
        q.put('CYTRYNY')
        q.put('SOK')

        loadcategories_screen.Update_Values_To_Categorise(q)
        
        self.manager.current = 'LoadCategoriesScreen'