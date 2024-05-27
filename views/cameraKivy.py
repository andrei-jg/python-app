from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from views import utils
import time, json

class CaptureARView(Screen):
    def __init__(self, **kwargs):
        super(CaptureARView, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0/1000.0)  # Actualiza cada 1/30 de segundo (30 fps)
        data_resolution = utils.send_uri(method='GET', payload=[], endpoint='get-resolution')['message']
        self.resolution = (data_resolution['height'], data_resolution['weight'])
        self.matrix, self.dist = utils.read_camera_calibration_params()
        
        # No accedas a la instancia de la cámara aquí
        # Accede a la cámara después de que la vista esté completamente construida
        self.camera_instance = None

    def on_enter(self, *args):
        super(CaptureARView, self).on_enter(*args)
        # Ahora que la vista está completamente construida, puedes acceder a la instancia de la cámara
        self.camera_instance = self.ids.camera
        self.manager.current = 'processed_frame_view'

    def update(self, dt):
        if self.camera_instance:
            # Lee el frame actual de la cámara
            camera = self.camera_instance

            time_init = time.time()
            texture = utils.detect_markers(camera, self.resolution, self.matrix, self.dist)
            self.manager.get_screen('processed_frame_view').update_texture(texture)
            print("Total time: ", time.time() - time_init)
            print("")