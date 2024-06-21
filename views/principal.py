# views/principal.py

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

from views import utils

class PrincipalView(Screen):
    user_email = StringProperty('')
    user_name = StringProperty('')

    def on_enter(self):
        # Aquí puedes usar el email para personalizar la vista principal
        payload = { "email": self.user_email }
        response_uri= utils.send_uri(method='GET', payload=payload, endpoint='get-profile')

        print(response_uri)
        self.user_name = response_uri['message']['name']
        
        # Obtener la instancia de LoginView y llamar a start_clock
        login_view = self.manager.get_screen('login_view')  # 'login_view' es el nombre de la pantalla de login
        # login_view.start_clock()