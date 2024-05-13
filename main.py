from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import numpy as np
import cv2
import requests
import time

Builder.load_string('''
<MyLayout>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: True
    ProcessedFrame:
        id: processed_frame
''')

class ProcessedFrame(Image):
    pass

class MyLayout(BoxLayout):
    pass

class MyApp(App):
    counter = 0
    uri = "http://192.168.39.124:5000/"

    def build(self):
        layout = MyLayout()
        self.cam = layout.ids.camera
        # self.marker_size_label = layout.ids.marker_size_label
        self.processed_frame = layout.ids.processed_frame
        Clock.schedule_once(self.detect_markers, 5)
        return layout

    def detect_markers(self, dt):
        frame = self.cam.texture
        if frame:
            frame = frame.pixels
            
            w, h = self.cam.resolution
            frame = np.frombuffer(frame, 'uint8').reshape(h, w, 4)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGBA2GRAY)


            # ------
            _, jpeg_frame = cv2.imencode('.jpg', gray)
            
            # Enviar la solicitud POST al servidor
            time_init = time.time()

                
            response = requests.post(
                f'{self.uri}/convertir_a_pixels', 
                data=jpeg_frame.tobytes(), 
                headers={'Content-Type': 'image/jpeg'}
            )

            # Decodificar la respuesta del servicio
            imagen_data = response.content

            # Decodificar los datos de la imagen en formato numpy array
            imagen_np = np.frombuffer(imagen_data, np.uint8)

            # Decodificar el numpy array en una imagen OpenCV
            imagen_cv = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)

            # ------

            frame = imagen_cv

            # Tu código existente
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

            # Hacer un flip en el eje y
            frame_flipped = cv2.flip(frame, 0)

            # Convertir la imagen al formato necesario para la textura
            buf = frame_flipped.tostring()

            # Resto de tu código
            texture = Texture.create(size=(w, h), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

            
            self.processed_frame.texture = texture


            Clock.schedule_once(self.detect_markers, 0.05)

if __name__ == "__main__":
    time_init = time.time()
    MyApp().run()
    time_end = time.time()
    print("END")
    print(time_end - time_init)
    