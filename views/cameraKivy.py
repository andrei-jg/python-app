from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from views.utils import utils
import time, os

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
        
        self.sound = SoundLoader.load(self.get_song_service())
        self.is_init_song = True
        self.play_song()

    def on_leave(self, *args):
        super(CaptureARView, self).on_leave(*args)

    def stop_update(self):
        # Detener la actualización
        Clock.unschedule(self.update)

    def update(self, dt):

        if self.is_init_song:
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
        self.delete_mp3_downloaded()
        if self.sound:
            self.sound.play()

    def get_song_service(self) -> str:

        response = utils.send_uri(method='GET', payload={'song': f'{utils.mp3_title}'}, endpoint='get-mp3')
        mp3_path = utils.get_path(utils.mp3_title)
        with open(mp3_path, 'wb') as file:
            file.write(response.content)

        return mp3_path
    
    def delete_mp3_downloaded(self):

        mp3_path = utils.get_path(utils.mp3_title)
        try:
            os.remove(mp3_path)
        except:
            pass