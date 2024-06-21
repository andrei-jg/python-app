import threading
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from views import utils
import time, json

class CaptureARView(Screen):
    def __init__(self, **kwargs):
        super(CaptureARView, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1.0/1000.0)  # Actualiza cada 1/30 de segundo (30 fps)
        data_resolution = utils.send_uri(method='GET', payload=[], endpoint='get-resolution')['message']
        self.resolution = (data_resolution['height'], data_resolution['weight'])
        self.matrix, self.dist = utils.read_camera_calibration_params()

        # Variables que se estarán alternando dependiendo la canción
        self.title = ""
        self.chords_of_title = ""
        self.int_position_chord = 0
        
        # Creamos el hilo pero no se inicializa aún
        self.update_chords_thread = threading.Thread(target=self.update_chords)
        self.update_chords_thread.daemon = True

        # Se instancia la cámara
        self.camera_instance = None

    def on_enter(self, *args):
        super(CaptureARView, self).on_enter(*args)
        # Ahora que la vista está completamente construida, puedes acceder a la instancia de la cámara
        index = utils.get_index_camera()
        self.camera_instance = self.ids.camera
        self.camera_instance.index = index
        self.manager.current = 'processed_frame_view'

        # Iniciamos el hilo de actualización de acordes cuando se entra en la vista
        utils.thread_flag = True
        if not self.update_chords_thread.is_alive():
            self.update_chords_thread.start()

    def on_leave(self, *args):
        super(CaptureARView, self).on_leave(*args)
        utils.thread_flag = False

    def update(self, dt):
        if self.camera_instance:
            utils.thread_flag = True
            # Lee el frame actual de la cámara
            camera = self.camera_instance

            time_init = time.time()
            texture = utils.detect_markers(camera, self.resolution, self.matrix, self.dist, self.chords_of_title)
            self.manager.get_screen('processed_frame_view').update_texture(texture)
            # print("Total time: ", time.time() - time_init)
            # print("")

    def update_chords(self):
        # while True:
            # utils.update_chords(dict_chord={})
            
        self.title = "rem-losing_my_religion.json"
        chords_data = utils.send_uri('GET', {"song": self.title}, 'get-song')
        chords_data = chords_data['message']['tracks'][1]["Guitar 2"]

        self.int_position_chord # Este tiene que ser incrementado... 

        total_elements = len(chords_data)
        print("Total de elementos en chords_data:", total_elements)

        for chord in chords_data:
            # Verificamos la bandera antes de actualizar self.chord
            if utils.thread_flag:
            
                # Actualizamos self.chord con los datos actuales
                self.chords_of_title = chord['notes']

                # Esperamos la duración especificada en los datos
                time.sleep(chord['time'] * 5)

                # Para efectos de depuración
                # print(f"Updated chord: {self.chords_of_title}, sleeping for {chord['duration']} seconds")
