from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.widget import Widget

import numpy as np
import cv2

class CaptureARView(Screen):
    def __init__(self, **kwargs):
        super(CaptureARView, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0/30.0)  # Actualiza cada 1/30 de segundo (30 fps)
        
        # No accedas a la instancia de la cámara aquí
        # Accede a la cámara después de que la vista esté completamente construida
        self.camera_instance = None

    def on_enter(self, *args):
        super(CaptureARView, self).on_enter(*args)
        # Ahora que la vista está completamente construida, puedes acceder a la instancia de la cámara
        self.camera_instance = self.ids.camera

    def update(self, dt):
        # Verifica si se ha inicializado la instancia de la cámara
        if self.camera_instance:
            # Lee el frame actual de la cámara

            camera = self.camera_instance

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