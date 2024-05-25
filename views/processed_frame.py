from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image

class ProcessedFrame(Screen):
    def __init__(self, **kwargs):
        super(ProcessedFrame, self).__init__(**kwargs)
        self.image = Image()
        self.add_widget(self.image)

    def update_texture(self, texture):
        self.image.texture = texture
