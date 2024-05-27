from kivy.utils import platform
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture

import requests, cv2, time, os, json, numpy as np, pickle

url = 'https://andrei00.pythonanywhere.com/api/'
marker_real_size = 5.0
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
parameters = cv2.aruco.DetectorParameters_create()

def send_uri(method: str, payload: dict, endpoint: str) -> dict:
    """
    Sends an HTTP request to the specified endpoint with the given method and payload.

    Args:
        method (str): The HTTP method to use ('GET', 'POST', 'PUT').
        payload (dict): The JSON payload to send with the request.
        endpoint (str): The endpoint URL to send the request to.

    Returns:
        dict: The JSON response from the server, with the status code included.

    Raises:
        ValueError: If the provided method is not one of 'GET', 'POST', 'PUT'.
        requests.exceptions.RequestException: If an error occurs during the HTTP request.
    """
    
    methods = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put
    }

    if method not in methods:
        raise ValueError(f"Invalid HTTP method: {method}. Must be one of 'GET', 'POST', 'PUT'.")

    try:
        response = methods[method](url + endpoint, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise  # Re-raise the exception after logging

    status_code = response.status_code

    try:
        decoded_response = response.json()
    except json.JSONDecodeError:
        decoded_response = {}  # Handle cases where the response is not JSON
    decoded_response['status_code'] = status_code

    return decoded_response

def read_camera_calibration_params() -> tuple[np.ndarray, np.ndarray]:
    # Carga el diccionario desde el archivo usando pickle
    with open('views/extra/calibration_data_pixel.pkl', 'rb') as file:
        calibration_data = pickle.load(file)

    # Extrae los datos del diccionario
    camera_matrix: np.ndarray = calibration_data['camera_matrix']
    dist_coeffs: np.ndarray = calibration_data['dist_coeffs']

    return (camera_matrix, dist_coeffs)

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

def draw_marker_detected(frame: cv2.UMat, marker_IDs: any, marker_corners: any, 
                         coefficients_matrix: np.ndarray, distortion_coefficients: np.ndarray):
    try:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners, 0.02, coefficients_matrix, distortion_coefficients)
        for rvec, tvec in zip(rvecs, tvecs):

            # cv2.drawFrameAxes(frame, coefficients_matrix, distortion_coefficients, rvec, tvec, 0.03)

            point_3d = np.array([[0.0332, 0.00, 0.00]], dtype=np.float32)
            # Proyectar el punto en el sistema de coordenadas de la cámara
            point_2d, _ = cv2.projectPoints(point_3d, rvec, tvec, coefficients_matrix, distortion_coefficients)
            
            # Convertir a enteros para dibujar
            point_2d = point_2d.reshape(-1, 2)
            point_2d = tuple(map(int, point_2d[0]))

            # Dibujar el punto en la imagen
            cv2.circle(frame, point_2d, 5, (0, 0, 255), -1)
    except cv2.error as e:
        print(f"OpenCV error: {e}")    

    return frame

def detect_markers(camera: Camera, resolution: tuple[int, int], matrix, dist):
    """
    Detects markers in the given camera feed at the specified resolution.

    Args:
        camera (Camera): The camera object from which the video feed is obtained.
        resolution (tuple[int, int]): A tuple specifying the resolution as (height, width).

    Returns:
        Texture: A Kivy texture object with the detected markers drawn on it.
    """
 
    texture = camera.texture
    size = texture.size  # e.g., (width, height)
    pixels = texture.pixels  # e.g., bytes object with pixel data

    image_bgr = np.frombuffer(pixels, dtype=np.uint8).reshape(size[1], size[0], 4)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_RGBA2RGB)
    if platform == 'android':
        image_rgb = cv2.flip(cv2.rotate(image_rgb, cv2.ROTATE_90_COUNTERCLOCKWISE), 0)
    image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGBA2GRAY)

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(image_gray, aruco_dict, parameters=parameters)
    if corners:
        # image_rgb = draw_marker_detected(image_rgb, ids, corners)
        image_rgb = draw_marker_detected(frame=image_rgb, marker_IDs=ids, marker_corners=corners, 
                                                coefficients_matrix=matrix, distortion_coefficients=dist)

    if platform == 'android':
        image_rgb = cv2.resize(image_rgb, (resolution[1], resolution[0]))     #  # (1080, 1920)

    buf = cv2.flip(image_rgb, 0).tobytes()
    h, w, channels = image_rgb.shape
    
    new_texture = Texture.create(size=(w, h), colorfmt='rgb')
    new_texture.blit_buffer(buf, bufferfmt="ubyte", colorfmt="rgb")

    return new_texture

if __name__ == "__main__":

    data = {
    "email": "a.jimenezgr@gmail.com",
    "password": "Mexico.1"
    }

    print(send_uri(method='POST', payload=data, endpoint='login'))