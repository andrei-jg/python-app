# views/principal.py

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

from views.utils import api

class PrincipalView(Screen):
    user_email = StringProperty('')
    user_name = StringProperty('')

    def on_enter(self):
        # Aquí puedes usar el email para personalizar la vista principal
        payload = { "email": self.user_email }
        send_uri = api.send_uri(method='GET', payload=payload, uri='get-profile')

        print(send_uri)
        self.user_name = send_uri['message']['name']
        