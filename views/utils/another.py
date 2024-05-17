from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.clock import Clock

from kivy.uix.widget import Widget
import numpy as np
import cv2

from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
import numpy as np
import cv2
import requests
import time
from kivy.utils import platform
import os

class MainApp(App):

    def build(self):
        # Crea la instancia de la cámara con una resolución más alta
        self.camera = Camera(play=True, index=0, resolution=(720, 480))
        # No la agregues a la interfaz de usuario
        # en lugar de eso, retorna un widget Label
        return Label(text="La cámara se está ejecutando en segundo plano")
    
    def save_picture(self) -> str:
        timestr = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"IMG_{timestr}.png"
        if platform == 'android':
            # Obtener la ruta de la carpeta DCIM
            dcim_path = os.path.join(os.environ['EXTERNAL_STORAGE'], 'DCIM')
            file_path = os.path.join(dcim_path, file_name)
        else:
            file_path = file_name  # Si no es Android, solo usa el nombre del archivo

        return file_path

    def on_start(self):
        # Espera un breve momento antes de intentar acceder a las dimensiones de la cámara
        Clock.schedule_once(self.detect_markers, 1)

    def detect_markers(self, dt):
            
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''

        # print("Height:", self.camera.texture.height)
        # print("Width:", self.camera.texture.width)

        camera = self.camera

        # print(camera)
        # <kivy.uix.camera.Camera object at 0x000001504292C190>


        file_name = 'IMG_.png'
        ### 1. Image - Con calidad ###            


        # image_from_camera = Widget.export_as_image(camera)

        # print(camera.height)
        # print(camera.width)

        height, width = camera.texture.height, camera.texture.width
        print(height, width)

        newvalue = np.frombuffer(camera.texture.pixels, np.uint8)
        newvalue = newvalue.reshape(height, width, 4)
        gray = cv2.cvtColor(newvalue, cv2.COLOR_RGBA2GRAY)

        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if corners:
            print("Marker Detected")

            cv2.aruco.drawDetectedMarkers(gray, corners, ids)
            backtorgb = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
            # cv2.imwrite(file_name, backtorgb)
        

        # cv2.imwrite("image.png", gray)

        # img = Image(image_from_camera)
        # img.save(f'{file_name}_original.png')

        Clock.schedule_once(self.detect_markers, 0.05)

if __name__== "__main__":
    MainApp().run()
