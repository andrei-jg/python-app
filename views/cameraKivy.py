from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from views import utils

import time

class CaptureARView(Screen):
    def __init__(self, **kwargs):
        super(CaptureARView, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0/1000.0)  # Actualiza cada 1/30 de segundo (30 fps)
        
        # No accedas a la instancia de la cámara aquí
        # Accede a la cámara después de que la vista esté completamente construida
        self.camera_instance = None

    def on_enter(self, *args):
        super(CaptureARView, self).on_enter(*args)
        # Ahora que la vista está completamente construida, puedes acceder a la instancia de la cámara
        self.camera_instance = self.ids.camera
        # self.manager.current = 'login_view'

    def update(self, dt):
        if self.camera_instance:
            # Lee el frame actual de la cámara
            camera = self.camera_instance

            time_init = time.time()
            utils.detect_markers(camera)
            print("Total time: ", time.time() - time_init)
            print("\n")