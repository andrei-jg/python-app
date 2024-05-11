import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class HolaMundo(App):
    def build(self):
        # return Label(text='¡Hola Mundo!')
        return BoxLayout()

holaMundo = HolaMundo()
holaMundo.run()
