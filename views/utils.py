from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture

import requests, cv2, time, os, json, numpy as np

url = 'https://andrei00.pythonanywhere.com/api/'
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
parameters = cv2.aruco.DetectorParameters_create()

def send_uri(method: str, payload: dict, endpoint: str) -> dict:

    methods = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put
    }

    response = methods[method](url + endpoint, json=payload)
    status_code = response.status_code

    decoded_response = json.loads(response.content.decode('utf-8'))
    decoded_response['status_code'] = status_code

    return decoded_response

def get_path() -> str:
    timestr = time.strftime("%Y%m%d_%H%M%S")
    file_name = f"IMG_{timestr}.png"
    if platform == 'android':
        # Obtener la ruta de la carpeta DCIM
        dcim_path = os.path.join(os.environ['EXTERNAL_STORAGE'], 'DCIM')
        file_path = os.path.join(dcim_path, file_name)
    else:
        file_path = file_name  # Si no es Android, solo usa el nombre del archivo

    # return 'IMG.png'
    return file_path

def detect_markers(camera: Widget):
            
    '''
    Function to capture the images and give them the names
    according to their captured time and date.
    '''
    image_from_camera = Widget.export_as_image(camera)

    texture = image_from_camera.texture
    size = texture.size  # e.g., (width, height)
    pixels = texture.pixels  # e.g., bytes object with pixel data

    image_bgr = np.frombuffer(pixels, dtype=np.uint8).reshape(size[1], size[0], 4)
    if platform == 'android':
        x, y = 317, 726
        w, h = 807, 1440
        image_bgr = image_bgr[y:y+h, x:x+w]
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_RGBA2GRAY)

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(image_gray, aruco_dict, parameters=parameters)

    if corners:
        print("Marker Detected")
        cv2.aruco.drawDetectedMarkers(image_rgb, corners, ids)

    ###########################################
    # Convertir la imagen al formato necesario para la textura

    # image_rgba = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2RGBA)
    image_rgba = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGBA)
    frame_flipped = cv2.flip(image_rgba, 0)
    buf = frame_flipped.tobytes()
    
    new_texture = Texture.create(size=(size[0], size[1]), colorfmt='rgba')
    new_texture.blit_buffer(buf, bufferfmt="ubyte", colorfmt="rgba")

    print(texture)
    print(new_texture)

    return new_texture

if __name__ == "__main__":

    data = {
    "email": "a.jimenezgr@gmail.com",
    "password": "Mexico.1"
    }

    print(send_uri(method='POST', payload=data, endpoint='login'))