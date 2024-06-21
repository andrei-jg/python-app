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

class LoginView(Screen):
    login_user = ObjectProperty()
    login_password = ObjectProperty()
    is_camera_on = BooleanProperty(False)
    debug = BooleanProperty(False)

    path_image_login = os.path.join(os.getcwd(), "views/images/vrLogo.png")

    def __init__(self, **kwargs):
        super(LoginView, self).__init__(**kwargs)
        response_uri = utils.send_uri(method='GET', payload={}, endpoint='get-position-chords')
        self.debug = response_uri['message']['debug']

    def build(self):
        pass

    def validate_credential(self):

        # Si no hay error, pasar el email a PrincipalView
        # self.manager.get_screen('principal_view').user_email = 'a.jimenezgr@gmail.com'
        if self.debug:
            self.manager.current = 'capture_ar_view'
            return
        
        payload = {
            "email": self.login_user.text,
            "password": self.login_password.text
        }

        response_uri = utils.send_uri(method='POST', payload=payload, endpoint='login')
        print(response_uri)

        if 'error' in response_uri:
            show = P()
            show.text = response_uri['error']

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

    def switch_to_forgot_password(self):
        self.manager.current = 'forgot_password'