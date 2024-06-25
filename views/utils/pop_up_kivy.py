from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDIconButton, MDTextButton

from views.utils import utils

class PopupContent(BoxLayout):
    def __init__(self, message: str, mode: str, **kwargs):
        super(PopupContent, self).__init__(**kwargs)

        self.mode_functions = {
            'password': self.set_new_password,
            'history': self.set_history,
            'get_songs': self.set_get_songs,
            'set_speed': self.set_speed
        }

        self.orientation = 'vertical'
        self.spacing, self.padding = 10, 10
        self.message_label = Label(text=message)
        self.add_widget(self.message_label)
        self.mode_functions.get(mode)()
        self.popup = None

    def on_dismiss(self, instance):
        # Esta función se llamará cuando el Popup se cierre
        print("Popup cerrado")

    def set_new_password(self):
        self.text_input = MDTextField(
            hint_text="Contraseña", 
            password=True, 
            multiline=False,
            icon_right='eye-off')
        self.add_widget(self.text_input)
        self.confirm_button = Button(text="Confirmar")
        self.confirm_button.bind(on_press=self.change_password_service)
        self.add_widget(self.confirm_button)

    def set_history(self):
        scroll_view = ScrollView(size_hint=(1, None), size=(180, 150))
        grid_layout = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Añadir elementos al GridLayout
        for i in range(20):  # Puedes cambiar el rango para agregar más elementos
            btn = Button(text=f'Button {i+1}', size_hint_y=None, height=40)
            btn.bind(on_release=self.on_button_click)
            grid_layout.add_widget(btn)

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

    def set_get_songs(self):
        response = self.get_all_song_service()

        scroll_view = ScrollView(size_hint=(1, None), size=(180, 150))
        grid_layout = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Añadir elementos al GridLayout
        for song in response:  # Puedes cambiar el rango para agregar más elementos
            btn = Button(text=f'{song["title"]}', size_hint_y=None, height=40)
            btn.song_id = song['filename']  # Añadir una propiedad personalizada
            btn.bind(on_release=self.set_global_title)
            grid_layout.add_widget(btn)

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

    def set_global_title(self, button):
        utils.global_title = button.song_id
        self.popup.dismiss()

    def on_button_click(self, button):
        print(f'Selected: {button.text}, ID: {button.song_id}')
        # self.popup.dismiss()

    def test(self):
        pass

    def set_speed(self):

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, pos_hint= {'center_x': 0.5})

        low = MDIconButton(icon='speedometer-slow', pos_hint={'center_x': 0.5})
        low.bind(on_release=lambda x: self.on_button_press('button1'))

        normal = MDIconButton(icon='speedometer-medium', pos_hint={'center_x': 0.5})
        normal.bind(on_release=lambda x: self.on_button_press('button1'))

        up = MDIconButton(icon='speedometer-medium', pos_hint={'center_x': 0.5})
        up.bind(on_release=lambda x: self.on_button_press('button1'))
        
        button_layout.add_widget(low)
        button_layout.add_widget(normal)
        button_layout.add_widget(up)

        # Alineación de los botones horizontalmente en el centro
        button_layout.pos_hint = {'center_x': 0.5}

        # Agregar el BoxLayout horizontal al layout principal
        self.add_widget(button_layout)

        # Ejecutar la función según el modo

        
    def change_password_service(self, instance):
        payload = {'email': utils.email_user, 'new_password': self.text_input.text, 'challenge': False}
        response_reset_password = utils.send_uri(method="POST", payload=payload, endpoint='reset-password')
        utils.message_main = utils.process_message(response_reset_password)

        if self.popup:
            self.popup.dismiss()

    def get_all_song_service(self):
        payload = {'song': ''}
        response_get_all_songs = utils.send_uri(method="GET", payload=payload, endpoint='get-song')['message']
        return response_get_all_songs