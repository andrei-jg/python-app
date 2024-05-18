from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty

from views.register import LoginView

import time
import threading

class LoginView(Screen):

    def __init__(self, **kwargs):
        super(LoginView, self).__init__(**kwargs)

    def on_enter(self, *args):
        thread = threading.Thread(target=self.bleed)
        thread.daemon = True
        thread.start()