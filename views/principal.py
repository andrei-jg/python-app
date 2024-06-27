# views/principal.py

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from views.utils import utils
from views.utils.pop_up_kivy import PopupContent

class P(FloatLayout):
    popup = None  # Variable para almacenar la referencia al Popup
    text = StringProperty()

class PrincipalView(Screen):
    user_email = StringProperty('')
    user_name = StringProperty('')
    run_ar_active = False

    def on_enter(self):
        pass

    def select_song(self):
        self.run_ar_active = True
        self.pop_message_method(message='Selecciona 1 canción', method='get_songs')
        
    def run_set_interval_time(self):
        self.run_ar_active = False  
        self.pop_message_method(message='Selecciona la velocidad', method='set_speed')
    
    def run_instructions(self):
        utils.instructions = utils.send_uri(method="GET", payload={}, endpoint='get-instructions')['message']
        utils.instructions.reverse()
        for i in utils.instructions:
            self.pop_message_normal(i)

        # self.pop_message()

    def run_history(self):
        self.pop_message_method(message='Historial de música', method='history')

    def run_new_password(self):
        self.pop_message_method(message='Nueva contraseña', method='password')

    def run_logout(self):
        self.manager.current = 'login_view'

    def pop_message_method(self, message: str, method: str):
        content = PopupContent(message, method)

        views_long = ['get_songs', 'history']
        size = utils.get_pop_up_size() if method not in views_long else (
            utils.get_pop_up_size()[0] + 100, utils.get_pop_up_size()[1] + 300)
        popupWindow = Popup(
            title="", 
            content=content, 
            size_hint=(None, None),
            size=size)
        
        content.popup = popupWindow
        popupWindow.bind(on_dismiss=self.pop_message)  # Vincula el evento on_dismiss

        if self.run_ar_active:
            popupWindow.bind(on_dismiss=lambda x: self.run_set_interval_time())

        popupWindow.open()

    def pop_message(self, instance):
        if utils.message_main == '':
            return
        if utils.message_main == 'Start AR':
            utils.message_main = ''
            self.manager.current = 'capture_ar_view'
            return

        show = P()
        show.text = utils.wrap_text(utils.message_main, 5)

        popupWindow = Popup(
            title="", 
            content=show, 
            size_hint=(None, None),
            size=utils.get_pop_up_size())
        
        show.popup = popupWindow
        popupWindow.open()

    def pop_message_normal(self, txt: str):
        show = P()
        show.text = utils.wrap_text(txt, 5)

        popupWindow = Popup(
            title="", 
            content=show, 
            size_hint=(None, None),
            size=utils.get_pop_up_size())
        
        show.popup = popupWindow
        popupWindow.open()