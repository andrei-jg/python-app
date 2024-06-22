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
        response_get_position_chords = utils.send_uri(method='GET', payload={}, endpoint='get-position-chords')
        response_pop_up_size = utils.send_uri(method='GET', payload={}, endpoint='get-resolution')['message']
        
        utils.pop_up_size = (response_pop_up_size['pop_up_android_x'], response_pop_up_size['pop_up_android_y'])
        self.debug = response_get_position_chords['message']['debug']

    def build(self):
        pass

    def validate_credential(self):

        if self.debug:
            self.manager.current = 'capture_ar_view'
            return
        
        payload = {
            "email": self.login_user.text,
            "password": self.login_password.text
        }

        response_login = utils.send_uri(method='POST', payload=payload, endpoint='login')
        print(response_login)

        if 'error' in response_login:
            show = P()
            show.text = response_login['error']

            popupWindow = Popup(
                title="Error", 
                content=show, 
                size_hint=(None, None),
                size=utils.get_pop_up_size())
            
            show.popup = popupWindow
            popupWindow.open()
            return

        # Si no hay error, pasar el email a PrincipalView
        self.manager.get_screen('principal_view').user_email = self.login_user.text
        self.manager.current = 'principal_view'

    def switch_to_forgot_password(self):
        self.manager.current = 'forgot_password'