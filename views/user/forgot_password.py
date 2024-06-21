from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.popup import Popup
from kivymd.uix.textfield import MDTextField

from views import utils

import os

class P(FloatLayout):
    popup = None  # Variable para almacenar la referencia al Popup
    text = StringProperty()

class ForgotView(Screen):
    path_image_login = os.path.join(os.getcwd(), "views/images/vrLogo.png")
    login_user = ObjectProperty()
    new_password_user = ObjectProperty()

    button_text = StringProperty()
    hint_text = StringProperty()

    email = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.new_password_field = None  # Almacenar referencia aquí


    def build(self):
        pass

    def on_enter(self, *args):
        self.hint_text = "Correo"
        self.button_text = "Recuperar contraseña"

    def password_recovery(self):
        text_field = self.login_user.text

        if self.hint_text == 'Correo':
            payload = {'email': text_field}
            response = utils.send_uri(method="POST", payload=payload, endpoint='reset-password-challenge')
            message = utils.process_message(response)

            if 'error' not in response:
                self.email = text_field
                self.login_user.text = ''
                self.hint_text = 'Código de seguridad'
                self.button_text = "Actualizar contraseña"
                self.ids.new_password_user.add_widget(self.set_password_field())
            self.pop_message(message=message)
        
        elif self.hint_text == 'Código de seguridad':
            if self.new_password_user.children:
                last_field = self.new_password_user.children[-1]
                new_password_str = last_field.text
                payload = {'email': self.email, 'code': text_field, 'new_password': new_password_str, 'challenge': True}
                response = utils.send_uri(method="POST", payload=payload, endpoint='reset-password')
                message = utils.process_message(response)
                print(response)

                self.pop_message(message=message)
                self.switch_to_login()

    def switch_to_login(self):
        self.hint_text = "Correo"
        self.button_text = "Recuperar contraseña"
        self.delete_password_field()

        self.manager.current = 'login_view'

    def pop_message(self, message: str):
        show = P()
        show.text = utils.wrap_text(message, 5)

        popupWindow = Popup(
            title="", 
            content=show, 
            size_hint=(None, None),
            size=(400, 250))
        
        show.popup = popupWindow
        popupWindow.open()

    def set_password_field(self) -> MDTextField:

        new_field = MDTextField(
            id='new_password',
            mode='round',
            hint_text="Contraseña",
            icon_right='eye-off',
            size_hint=(0.95, None),
            height='48dp',
            font_size='16sp',
            pos_hint={'center_x': 0.5},
            password=True
        )
        self.new_password_field = new_field  # Almacenar referencia
        return new_field
    
    def delete_password_field(self) -> None:
        if self.new_password_field:
            self.ids.new_password_user.remove_widget(self.new_password_field)
            self.new_password_field = None  # Limpiar la referencia
