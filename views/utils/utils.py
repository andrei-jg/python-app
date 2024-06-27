from kivy.utils import platform
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture

import requests, cv2, time, os, json, numpy as np, pickle
from datetime import datetime

url = 'https://andrei00.pythonanywhere.com/api/'
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
parameters = cv2.aruco.DetectorParameters_create()
pixel = True
pop_up_size = (0,0)

email_user, name_user, message_main = "", "", ""
email_user = "a.jimenezgr@gmail.com"
instructions = []
idx_instructions = 0

# Variables que se estarán alternando dependiendo la canción
global_title = "10_Soda Stereo - De Música Ligera (ver 2).json"
multipler_time = 1.0
mp3_title = ""

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

    response = methods[method](url + endpoint, json=payload)

    if endpoint == 'calibration-file' or endpoint == 'get-mp3':
        return response

    status_code = response.status_code

    try:
        decoded_response = response.json()
    except json.JSONDecodeError:
        decoded_response = {}  # Handle cases where the response is not JSON
    decoded_response['status_code'] = status_code

    print("")
    print("----")
    print("Endpoint:", endpoint)
    print("Método:", method)
    print("Payload enviado: ", payload)
    print("Response: ", decoded_response)
    print("----")
    print("")

    return decoded_response

def find_chord(input_notes: str) -> str | None:
    """
    Encuentra el acorde que mejor coincida con el str de entrada.

    Args:
        input_notes (str): String de notas separadas por comas.

    Returns:
        best_match (str): Nombre del acorde que mejor coincide.
    """
    global chords
    best_match = None
    min_matches = 4  # Minimum exact matches required
    min_difference = float('inf')

    for chord, value in chords.items():
        # Split chord values into a list of notes
        if value == "chord":
            return best_match

        # print(input_notes)
        chord_notes = str(value['chord'])
        chord_notes = chord_notes.split(',')
        input_notes_list = input_notes.split(',')

        # Check if lengths of lists are same
        if len(chord_notes) != len(input_notes_list):
            continue

        # Calculate the difference between notes
        difference = sum(1 for chord_note, input_note in zip(chord_notes, input_notes_list) if chord_note != 'X' and chord_note != input_note)

        # If difference is less than or equal and at least 3 notes match exactly
        if difference <= min_difference:
        # Verificar si el número de notas que coinciden exactamente es igual o mayor que el mínimo requerido
            exact_matches = sum(1 for chord_note, input_note in zip(chord_notes, input_notes_list) if chord_note != 'X' and chord_note == input_note)
            if exact_matches >= min_matches:
                # Actualizar la mejor coincidencia si se cumple la condición
                min_difference = difference
                best_match = chord

    return best_match

def center_text(text: str, start_x: int, start_y: int):
    """
    Centra un texto en una imagen.

    Args:
        texto (str): Texto que se va a centrar.
        start_x (int): Coordenada X para comenzar a centrar.
        start_y (int): Coordenada Y para comenzar a centrar.

    Returns:
        tuple: Coordenadas X e Y del texto centrado.
    """
    font_scale = 1
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Get text size
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness=1)
    
    # Calculate position to center text
    text_x = start_x - text_width // 2
    text_y = start_y + text_height // 2
    
    return text_x, text_y

def draw_chord(actual_chord: str) -> cv2.UMat:
    """
    Dibuja un diagrama de acorde.

    Args:
        actual_chord (str): Nombre del acorde.
        diagram_chords_data (dict): Diccionario que contiene información del acorde y los dedos.
    """
    # Create a blank white image
    img = np.ones((200, 200, 3), np.uint8) * 255
    
    # Basic coordinates and dimensions
    start_x, start_y = 50, 50
    width, height = 100, 100
    string_spacing = width // 5
    fret_spacing = height // 5

    # Draw strings
    for i in range(6):
        x = start_x + i * string_spacing
        cv2.line(img, (x, start_y), (x, start_y + height), (0, 0, 0), 2)

    # Draw frets
    for i in range(6):
        y = start_y + i * fret_spacing
        cv2.line(img, (start_x, y), (start_x + width, y), (0, 0, 0), 2)

    # Draw chord dots and numbers
    global chords
    is_defined_actual_chord = find_chord(actual_chord)
    
    if is_defined_actual_chord:
        name_str_actual_chord = is_defined_actual_chord
        chord = chords[name_str_actual_chord]["chord"].split(',')
        fingers = chords[name_str_actual_chord]["fingers"].split(',')
    else:
        name_str_actual_chord = ""
        chord = actual_chord.split(',')
        fingers = "........"

    for i, (fret, finger) in enumerate(zip(chord, fingers)):
        if fret != 'X':
            fret = int(fret)
            if fret != 0:
                x = start_x + i * string_spacing
                y = start_y + fret * fret_spacing - fret_spacing // 2
                cv2.circle(img, (x, y), 8, (0, 0, 0), -1)
                # Add fret number and finger position
                cv2.putText(img, str(finger), (x - 5, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            else:
                x = start_x + i * string_spacing
                y = start_y - 20
                cv2.putText(img, 'O', (x-10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    text_x, text_y = center_text(name_str_actual_chord, 100, 175)
    cv2.putText(img, name_str_actual_chord, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    if platform == 'android':
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    return img

def get_position_note(note: int, string: int):
    """
    Devuelve la coordenada x, y, z de la nota que se está procesando.

    Args:
        note (int): Nota a procesar.
        string (int): Cuerda donde se deberá visualizar la nota.
    """
    global all_position_chords
    mapping = {
        1: -0.009,
        2: -0.005,
        3: 0.0015,
        4: 0.005,
        5: 0.0085,
        6: 0.013
    }
    new_chord = all_position_chords['positions'] # Gives middle: Between string 6 and 1

    try:
        x = float(new_chord[note]['x']) + float(mapping.get(string, 0))
        y = float(new_chord[note]['y'])
        z = float(new_chord[note]['z'])
    except:
        x = y= z = -0.1

    debug = all_position_chords['debug_chord']
    if debug:
        x = float(new_chord["1"]['x'])
        y = float(new_chord["1"]['y'])
        z = float(new_chord["1"]['z'])

    return x, y, z

def join_frame_diagram(frame: cv2.UMat, guitar_diagram: cv2.UMat) -> cv2.UMat:

    # Obtener las dimensiones del frame y de la textura
    frame_height, frame_width, _ = frame.shape
    texture_height, texture_width, _ = guitar_diagram.shape

    # Definir la posición donde se va a colocar la textura
    top_left_y = 0
    top_left_x = frame_width - texture_width

    if platform == "android":
        top_left_y = frame_height - texture_height
        top_left_x = frame_width - texture_width

    # Crear una máscara para la textura (asumiendo que tiene un canal alfa)
    if guitar_diagram.shape[2] == 4:  # Si la textura tiene un canal alfa
        alpha_mask = guitar_diagram[:, :, 3] / 255.0
        alpha_mask = cv2.merge([alpha_mask, alpha_mask, alpha_mask])
        texture_rgb = guitar_diagram[:, :, :3]
    else:
        alpha_mask = np.ones_like(guitar_diagram, dtype=float)
        texture_rgb = guitar_diagram

    # Recortar la parte del frame donde se superpondrá la textura
    roi = frame[top_left_y:top_left_y + texture_height, top_left_x:top_left_x + texture_width]

    # Combinar la textura con el frame usando la máscara alfa
    combined = roi * (1 - alpha_mask) + texture_rgb * alpha_mask

    # Colocar la imagen combinada de nuevo en el frame
    frame[top_left_y:top_left_y + texture_height, top_left_x:top_left_x + texture_width] = combined

    return frame

def read_camera_calibration_params() -> tuple[np.ndarray, np.ndarray]:

    device = "calibration_data_work" if pixel else "calibration_data_pc"
    payload = {"device": device}

    calibration_response = send_uri(method='GET', payload=payload, endpoint='calibration-file')
    calibration_data = pickle.loads(calibration_response.content)

    # Extrae los datos del diccionario
    camera_matrix: np.ndarray = calibration_data['camera_matrix']
    dist_coeffs: np.ndarray = calibration_data['dist_coeffs']

    return (camera_matrix, dist_coeffs)

def get_index_camera() -> int:
    return 0 if pixel else 1

def get_path(filename: str) -> str:
    
    if platform == 'android':
        # Obtener la ruta de la carpeta DCIM
        dcim_path = os.path.join(os.environ['EXTERNAL_STORAGE'], 'DCIM')
        file_path = os.path.join(dcim_path, filename)
    else:
        file_path = filename  # Si no es Android, solo usa el nombre del archivo

    return file_path

def draw_marker_detected(frame: cv2.UMat, marker_IDs: any, marker_corners: any, 
                         coefficients_matrix: np.ndarray, distortion_coefficients: np.ndarray, chord: str):
    global all_position_chords
    for marker_id in marker_IDs:
        pass
        # print(f"Detected marker ID: {marker_id[0]}")
    try:
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(marker_corners, 0.02, coefficients_matrix, distortion_coefficients)
        for rvec, tvec in zip(rvecs, tvecs):

            # Dibuja los ejes
            if all_position_chords['draw_axis']:
                cv2.drawFrameAxes(frame, coefficients_matrix, distortion_coefficients, rvec, tvec, 0.03)

            for rvec, tvec in zip(rvecs, tvecs):
            # Verificar y corregir el valor del eje Z
                if tvec[0][2] < 0:
                    tvec[0][2] = -tvec[0][2]
                    print(f"Inverted Z detected. Corrected Z: {tvec[0][2]}")

            note = chord.replace(",","")
            for string, i in enumerate(note, start=1):
                if i != 'X':
                    x, y, z = get_position_note(note=i, string=string)

                    point_3d = np.array([[x, y, z]], dtype=np.float32)
                    
                    point_2d, _ = cv2.projectPoints(point_3d, rvec, tvec, coefficients_matrix, distortion_coefficients)
                    point_2d = point_2d.reshape(-1, 2)
                    point_2d = tuple(map(int, point_2d[0]))
                    cv2.circle(frame, point_2d, 4, (0, 0, 255), -1)

    except cv2.error as e:
        print(f"OpenCV error: {e}")

    return frame

def detect_markers(camera: Camera, resolution: tuple[int, int], matrix: np.ndarray, 
                   dist: np.ndarray, chord:str):
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
        image_rgb = draw_marker_detected(frame=image_rgb, marker_IDs=ids, marker_corners=corners, 
                                                coefficients_matrix=matrix, distortion_coefficients=dist, chord=chord)
    diagram_chord = draw_chord(actual_chord=chord)
    image_rgb = join_frame_diagram(frame=image_rgb, guitar_diagram=diagram_chord)

    if platform == 'android':
        image_rgb = cv2.resize(image_rgb, (resolution[1], resolution[0]))     #  # (1080, 1920)

    buf = cv2.flip(image_rgb, 0).tobytes()
    h, w, channels = image_rgb.shape
    
    new_texture = Texture.create(size=(w, h), colorfmt='rgb')
    new_texture.blit_buffer(buf, bufferfmt="ubyte", colorfmt="rgb")

    return new_texture

def process_message(response: dict) -> str:

    if 'error' in response:
        message = response['error']
    else:
        message = response['message']

    return message

def wrap_text(text: str, max_words: int) -> str:
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        if len(current_line) == max_words:
            lines.append(' '.join(current_line))
            current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

def get_pop_up_size() -> tuple[int, int]:

    if platform == 'android':
        return pop_up_size
    else:
        return (300, 250)
    
def return_actual_chord_by_time(time_elapsed: float, all_song_chords: dict, total_time: float, tempo: int) -> str:

    global multipler_time
    time_elapsed = time.time() - time_elapsed

    if time_elapsed > total_time:
        return 'end'

    song_elapsed = 0.0
    for chord in all_song_chords:
        # Operación para calcular en segundos la duración del acorde - nota
        seconds = chord['time'] * 60 / int(tempo * multipler_time)
        song_elapsed += seconds
        # print(chord, seconds, song_elapsed)
        if song_elapsed >= time_elapsed:
            print(song_elapsed, chord['notes'], time_elapsed)
            return chord['notes']

def get_total_time(all_song_chords: dict, tempo: int) -> float:
    """
    Regresa el total del tiempo que dura la canción en segundos

    Args:
        all_song_chords (dict): El diccionario de acordes de la música seleccionada.

    Returns:
        song_elapsed (float): El total en segundos que dura la canción.
    """
    global multipler_time
    song_elapsed = 0.0

    for chord in all_song_chords:
        # Operación para calcular en segundos la duración del acorde - nota
        seconds = chord['time'] * 60 / int(tempo * multipler_time)
        song_elapsed += seconds
        
    return song_elapsed

def set_chords_by_song(chord_by_song: dict, key: str) -> dict:
    """
    Asigna los acordes a interpretar por el sistema dependiendo la guitarra que en key delimitemos
    
    Args:
        key (str): La clave de identificación que tiene la guitarra a mostrar

    Returns:
        None
    """
    chord_by_song = chord_by_song['message']['tracks']

    for track in chord_by_song:
        if key in track:
            chord_by_song = track[key]

    return chord_by_song

def get_resolution_camera_root() -> tuple[int, int]:

    if platform == 'android':
        return (640, 480)
    else:
        return (640, 360)
    
def transform_timestamp_to_date(timestamp: float, format_date: str) -> str:
    dt_object = datetime.fromtimestamp(timestamp)

    key_date_form = {
        'day': '%Y-%m-%d',
        'time': '%Y-%m-%d %H:%M'
    }

    return dt_object.strftime(key_date_form.get(format_date))

if __name__ != "__main__":
    chords = send_uri("GET", [], "get-diagram-guitar")['message']
    all_position_chords = send_uri(method='GET', payload=[], endpoint='get-position-chords')['message']

if __name__ == "__main__":

    if instructions == []:
        response_get_instructions = send_uri(method="GET", payload={}, endpoint='get-instructions')['message']
        instructions = response_get_instructions
    

    print("Inicio: ", idx_instructions)

    idx_instructions = 2

    if idx_instructions + 1 > len(instructions):
        instructions = []
        idx_instructions = 0
        message_main = ""
    else:
        message_main = instructions[idx_instructions]
        idx_instructions += 1

    print(message_main, idx_instructions)        



