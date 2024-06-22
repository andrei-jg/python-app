# views/login.py

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from views import utils
import os

class P(FloatLayout):
    popup = None  # Variable para almacenar la referencia al Popup
    text = StringProperty()

class RegisterView(Screen):
    name_user = ObjectProperty()
    email_user = ObjectProperty()
    password_user = ObjectProperty()

    path_image_login = os.path.join(os.getcwd(), "views/images/vrLogo.png")

    def __init__(self, **kwargs):
        super(RegisterView, self).__init__(**kwargs)

    def build(self):
        pass

    def create_account(self):
        payload = {
            "name": self.name_user.text,
            "email": self.email_user.text,
            "password": self.password_user.text
        }
        response_register = utils.send_uri(method='POST', payload=payload, endpoint='register')
        message = utils.process_message(response_register)
        self.pop_message(message)

    def pop_message(self, message: str):
        show = P()
        show.text = utils.wrap_text(message, 5)

        popupWindow = Popup(
            title="", 
            content=show, 
            size_hint=(None, None),
            size=utils.get_pop_up_size())
        
        show.popup = popupWindow
        popupWindow.open()

    def switch_to_login(self):
        self.manager.current = 'login_view'
        self.name_user.text = ""
        self.email_user.text = ""
        self.password_user.text = ""