from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
import numpy as np
import cv2
import requests
import time
from kivy.utils import platform
import os

class ProcessedFrame(Image):
    pass

class MyLayout(BoxLayout):
    pass


class MyApp(App):
    counter = 0
    uri = "http://192.168.39.124:5000/"

    def get_path(self) -> str:
        timestr = time.strftime("%Y%m%d_%H%M%S")
        file_name = f"IMG_{timestr}.png"
        if platform == 'android':
            # Obtener la ruta de la carpeta DCIM
            dcim_path = os.path.join(os.environ['EXTERNAL_STORAGE'], 'DCIM')
            file_path = os.path.join(dcim_path, file_name)
        else:
            file_path = file_name  # Si no es Android, solo usa el nombre del archivo

        return file_path

    def build(self):
        layout = MyLayout()
        self.cam = layout.ids.camera
        # self.marker_size_label = layout.ids.marker_size_label
        self.processed_frame = layout.ids.processed_frame
        Clock.schedule_once(self.detect_markers, 5)
        return layout

    def detect_markers(self, dt):
            
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.cam
        file_name = self.get_path()

        print("camera.texture: ",
              camera.texture.width,
              camera.texture.height
              )

        ### 1. Image - Con calidad ###            

        image_from_camera = Widget.export_as_image(camera)
        # img = Image(image_from_camera)
        # img.save(f'{file_name}original_.png')


        height, width = image_from_camera.texture.height, image_from_camera.texture.width
        # print(height, width)
        # 690 1000
        
        newvalue = np.frombuffer(image_from_camera.texture.pixels, np.uint8)
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
        

        # frame = self.cam.texture

        # Tu código existente
        # frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)

        # Hacer un flip en el eje y
        # frame_flipped = cv2.flip(frame, 0)

        # Convertir la imagen al formato necesario para la textura
        """
        buf = gray.tostring()

        w = width
        h = height

        # Resto de tu código
        texture = Texture.create(size=(w, h), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

        
        self.processed_frame.texture = texture

        """


        Clock.schedule_once(self.detect_markers, 0.05)