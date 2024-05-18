# views/login.py

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

from views.utils import api
import os

class P(FloatLayout):
    popup = None  # Variable para almacenar la referencia al Popup
    text = StringProperty()

class LoginView(Screen):
    login_user = ObjectProperty()
    login_password = ObjectProperty()
    login_password = ObjectProperty()
    path_image_login = os.path.join(os.getcwd(), "views/images/vrLogo.png")

    def build(self):
        pass

    def validate_credential(self):

        # Si no hay error, pasar el email a PrincipalView
        self.manager.get_screen('principal_view').user_email = 'a.jimenezgr@gmail.com'
        self.manager.current = 'principal_view'
        return

        payload = {
            "email": self.login_user.text,
            "password": self.login_password.text
        }

        send_uri = api.send_uri(method='POST', payload=payload, uri='login')
        print(send_uri)

        if 'error' in send_uri:
            show = P()
            show.text = send_uri['error']

            popupWindow = Popup(
                title="Error", 
                content=show, 
                size_hint=(None, None),
                size=(300, 250))
            
            show.popup = popupWindow
            popupWindow.open()
            return

        # Si no hay error, pasar el email a PrincipalView
        self.manager.get_screen('principal_view').user_email = self.login_user.text
        self.manager.current = 'principal_view'