from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from views.utils import utils
import time, tempfile, io

class CaptureARView(Screen):
    def __init__(self, **kwargs):
        super(CaptureARView, self).__init__(**kwargs)
        data_resolution = utils.send_uri(method='GET', payload=[], endpoint='get-resolution')['message']
        self.resolution = (data_resolution['height'], data_resolution['weight'])
        self.matrix, self.dist = utils.read_camera_calibration_params()
        self.camera_resolution = utils.get_resolution_camera_root()
        
        # Se instancia la cámara
        self.camera_instance = None

    def on_enter(self, *args):
        self.sound = self.load_song()
        super(CaptureARView, self).on_enter(*args)
        Clock.schedule_interval(self.update, 1.0/1000.0)  # Actualiza cada 1/30 de segundo (30 fps)

        index = utils.get_index_camera()
        self.camera_instance = self.ids.camera
        self.camera_instance.index = index
        self.manager.current = 'processed_frame_view'

        # Variables que se estarán alternando dependiendo la canción
        self.chords_data: dict = utils.send_uri('GET', {"song": utils.global_title}, 'get-song')['message']
        self.tempo: int = self.chords_data['tempo']
        self.chord_by_song: dict = self.chords_data['tracks']
        key: str = 'base'

        for track in self.chord_by_song:
            if key in track:
                self.chord_by_song = track[key]
        
        self.total_time_song: float = utils.get_total_time(self.chord_by_song, self.tempo)
        
        self.is_init_song = True

    def on_leave(self, *args):
        super(CaptureARView, self).on_leave(*args)

    def stop_update(self):
        # Detener la actualización
        Clock.unschedule(self.update)

    def update(self, dt):

        if self.is_init_song:
            self.play_song()
            self.time_init = time.time()
            self.is_init_song = False
        
        if self.camera_instance:
            # Lee el frame actual de la cámara
            camera = self.camera_instance
            actual_chord = utils.return_actual_chord_by_time(self.time_init, self.chord_by_song, self.total_time_song, self.tempo)
            if actual_chord != 'end' and actual_chord != None:
                texture = utils.detect_markers(camera, self.resolution, self.matrix, self.dist, actual_chord)
                self.manager.get_screen('processed_frame_view').update_texture(texture)
            else:
                self.stop_update()
                self.manager.current = 'principal_view'

    def play_song(self):
        if self.sound:
            self.sound.play()

    def get_song_service(self) -> io.BytesIO:
        response = utils.send_uri(method='GET', payload={'song': f'{utils.mp3_title}'}, endpoint='get-mp3')
        
        buffer = io.BytesIO()
        buffer.write(response.content)
        buffer.seek(0)
        
        return buffer
    
    def load_song(self):
        attempts = 3  # Número de intentos máximos
        for attempt in range(1, attempts + 1):
            mp3_buffer = self.get_song_service()

            # Verificar la integridad del buffer comparando longitudes
            original_length = len(mp3_buffer.getvalue())

            # Crear un archivo temporal con extensión .mp3
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file.write(mp3_buffer.read())
                temp_file_path = temp_file.name

            # Leer el contenido del archivo temporal y comparar longitudes
            with open(temp_file_path, 'rb') as f:
                temp_file_content = f.read()
                temp_file_length = len(temp_file_content)

            # Comparar longitudes para asegurar la integridad
            if original_length != temp_file_length:
                if attempt < attempts:
                    print(f"Intento {attempt}: La longitud del buffer original y el archivo temporal no coinciden, reintentando...")
                    continue
                else:
                    raise RuntimeError(f"Se superó el número máximo de intentos ({attempts}). Posible pérdida de datos.")
            else:
                break  # Salir del bucle si la longitud es consistente

        return SoundLoader.load(temp_file_path)