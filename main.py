from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty
from kivymd.app import MDApp

from views.login import LoginView
from views.register import RegisterView
from views.principal import PrincipalView
from views.cameraKivy import CaptureARView
from views.processed_frame import ProcessedFrame

class Manager(ScreenManager):
    login_view = ObjectProperty(None)
    register_view = ObjectProperty(None)
    principal_view = ObjectProperty(None)
    capture_ar_view = ObjectProperty(None)
    processed_frame_view = ObjectProperty(None)

class ScreensApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        m = Manager(transition=NoTransition())
        return m

if __name__ == "__main__":
    ScreensApp().run()