from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.uix.image import Image

import requests, cv2, time, os, json, numpy as np

url = 'https://andrei00.pythonanywhere.com/api/'
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
parameters = cv2.aruco.DetectorParameters_create()

def send_uri(method: str, payload: dict, uri: str) -> dict:

    methods = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put
    }

    response = methods[method](url + uri, json=payload)
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

    return 'IMG.png'
    # return file_path

def detect_markers(camera):
            
    '''
    Function to capture the images and give them the names
    according to their captured time and date.
    '''

    time_init = time.time()
    file_name = get_path()
    print("file_name: ", time.time() - time_init)

    time_init = time.time()
    image_from_camera = Widget.export_as_image(camera)
    height, width = image_from_camera.texture.height, image_from_camera.texture.width
    # print(height, width)
    print("image_from_camera: ", time.time() - time_init)
    # 750, 1000

    
    time_init = time.time()
    newvalue = np.frombuffer(image_from_camera.texture.pixels, np.uint8)
    newvalue = newvalue.reshape(height, width, 4)
    print("newvalue: ", time.time() - time_init)

    time_init = time.time()
    gray = cv2.cvtColor(newvalue, cv2.COLOR_RGBA2GRAY)
    print("gray: ", time.time() - time_init)
    

    time_init = time.time()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print("aruco_dict: ", time.time() - time_init)

    if corners:
        print("Marker Detected")

        time_init = time.time()
        cv2.aruco.drawDetectedMarkers(gray, corners, ids)

    backtorgb = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
    print("backtorgb: ", time.time() - time_init)


    # time_init = time.time()
    # cv2.imwrite(file_name, backtorgb)
    # print("imwrite: ", time.time() - time_init)



if __name__ == "__main__":

    data = {
    "email": "a.jimenezgr@gmail.com",
    "password": "Mexico.1"
    }


    print(send_uri(method='POST', payload=data, uri='login'))

