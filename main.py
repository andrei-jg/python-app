from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.core.image import Image
import numpy as np

import time, os, cv2

angle = 0
if platform == 'android':
    angle = -90

Builder.load_string(f'''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        index: 0
        id: camera
        resolution: (1920,1080)
        play: True
        allow_stretch: True
        canvas.before:
            PushMatrix
            Rotate:
                angle: {angle}
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

    def save_picture(self) -> str:
        timestr = time.strftime("%Y%m%d_%H%M%S")
        file_name = "IMG_{}.png".format(timestr)
        if platform == 'android':
            # Obtener la ruta de la carpeta DCIM
            dcim_path = os.path.join(os.environ['EXTERNAL_STORAGE'], 'DCIM')
            file_path = os.path.join(dcim_path, file_name)
        else:
            file_path = file_name  # Si no es Android, solo usa el nombre del archivo

        return file_path
        
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        file_name = self.save_picture()

        ### 1. Image - Con calidad ###            

        image_from_camera = Widget.export_as_image(camera)
        # img = Image(image_from_camera)
        # img.save(f'{file_name}original_.png')


        height, width = image_from_camera.texture.height, image_from_camera.texture.width
        print(height, width)
        # 690 1000
        
        newvalue = np.frombuffer(image_from_camera.texture.pixels, np.uint8)
        newvalue = newvalue.reshape(height, width, 4)
        gray = cv2.cvtColor(newvalue, cv2.COLOR_RGBA2GRAY)

        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
        parameters = cv2.aruco.DetectorParameters_create()
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if corners:
            print("OK")

            cv2.aruco.drawDetectedMarkers(gray, corners, ids)
            backtorgb = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
            cv2.imwrite(file_name, backtorgb)

class TestCamera(App):

    def build(self):
        return CameraClick()

TestCamera().run()