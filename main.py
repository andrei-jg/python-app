from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from android.permissions import request_permissions, Permission
import time
import os
from PIL import Image
import cv2
from io import BytesIO
from kivy.core.image import Image as CoreImage

request_permissions([
    Permission.CAMERA,
    Permission.WRITE_EXTERNAL_STORAGE,
    Permission.READ_EXTERNAL_STORAGE
])

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        index: 0
        id: camera
        resolution: (640,480)
        play: True
        allow_stretch: True
        canvas.before:
            PushMatrix
            Rotate:
                angle: -90
                origin: self.center
        canvas.after:
            PopMatrix
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')


class CameraClick(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        file_name = "IMG_{}.png".format(timestr)
        if platform == 'android':
            # Obtener la ruta de la carpeta DCIM
            dcim_path = os.path.join(os.environ['EXTERNAL_STORAGE'], 'DCIM')
            file_path = os.path.join(dcim_path, file_name)
        else:
            file_path = file_name  # Si no es Android, solo usa el nombre del archivo
        camera.export_to_png(file_path)
        print("Imagen guardada en:", file_path)

        # Leer la imagen con OpenCV
        image = cv2.imread(file_path)

        # Realizar operaciones de procesamiento de imagen con OpenCV
        # Por ejemplo, puedes convertir la imagen a escala de grises
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Mostrar la imagen procesada utilizando Kivy
        buf = BytesIO()
        Image.fromarray(gray_image).save(buf, format='png')
        buf.seek(0)
        img = CoreImage(BytesIO(buf.read()), ext='png')
        # Muestra la imagen procesada
        # Puedes usarla en un widget de imagen Kivy o guardarla como una imagen Kivy
        # image_widget.texture = img.texture

class TestCamera(App):

    def build(self):
        return CameraClick()


TestCamera().run()
