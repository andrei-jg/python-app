from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty
from kivymd.app import MDApp

from views.user.login import LoginView
from views.user.register import RegisterView
from views.user.forgot_password import ForgotView
from views.principal import PrincipalView
from views.cameraKivy import CaptureARView
from views.processed_frame import ProcessedFrame

from views.utils import utils
class Manager(ScreenManager):
    pass
class ScreensApp(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        m = Manager(transition=NoTransition())
        return m

if __name__ == "__main__":
    ScreensApp().run()