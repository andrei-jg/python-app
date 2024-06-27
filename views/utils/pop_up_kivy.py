from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDIconButton, MDTextButton

from views.utils import utils
import time

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
        print("Popup cerrado")

    def set_new_password(self):
        self.text_input = MDTextField(
            hint_text="Contraseña", 
            password=True, 
            multiline=False,
            icon_right='eye-off',
            height=100)
        self.add_widget(self.text_input)
        self.confirm_button = Button(text="Confirmar")
        self.confirm_button.bind(on_press=self.change_password_service)
        self.add_widget(self.confirm_button)

    def set_history(self):
        response = self.get_history_by_user_service()

        scroll_view = ScrollView(size_hint=(1, None), size=(100, 580))
        grid_layout = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        for song, times in response.items():
            for time in times:
                text = f"{song}: {utils.transform_timestamp_to_date(timestamp=time, format_date='day')}"
                btn = Button(text=text, size_hint_y=None, height=100)
                grid_layout.add_widget(btn)

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

    def set_get_songs(self):
        response = self.get_all_song_service()

        scroll_view = ScrollView(size_hint=(1, None), size=(50, 580))
        grid_layout = GridLayout(cols=1, padding=10, spacing=10, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        for song in response:
            btn = Button(text=f'{song["title"]}', size_hint_y=None, height=100)
            btn.song_id = song['filename']
            btn.bind(on_release=self.set_global_title)
            grid_layout.add_widget(btn)

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

    def set_global_title(self, button):
        utils.global_title = button.song_id
        self.add_history_by_user_service(title=button.text)
        self.popup.dismiss()

    def set_global_title(self, button):
        utils.global_title = button.song_id
        self.add_history_by_user_service(title=button.text)
        self.popup.dismiss()

    def set_speed(self):

        button_layout = BoxLayout(orientation='horizontal', pos_hint= {'center_x': 0.7})

        low = MDIconButton(icon='tortoise')
        low.bind(on_release=lambda x: self.on_button_press('low'))

        normal = MDIconButton(icon='speedometer-medium')
        normal.bind(on_release=lambda x: self.on_button_press('normal'))

        up = MDIconButton(icon='rabbit')
        up.bind(on_release=lambda x: self.on_button_press('up'))
        
        button_layout.add_widget(low)
        button_layout.add_widget(normal)
        button_layout.add_widget(up)

        self.add_widget(button_layout)

    def on_button_press(self, txt_button: str):
        key_speed = {
            'low': 1.5,
            'normal': 1.0,
            'up': 0.5
        }
        utils.multipler_time = key_speed.get(txt_button)
        utils.message_main = 'Start AR'

        # Se arma el archivo mp3 a descargar...
        split_json = utils.global_title.split('.json')[0]
        utils.mp3_title = f"{split_json}_{txt_button}.mp3"

        self.popup.dismiss()
        
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
    
    def get_history_by_user_service(self):
        payload = {'email': utils.email_user}
        return utils.send_uri(method="GET", payload=payload, endpoint='get-history')['message']
    
    def add_history_by_user_service(self, title: str):
        user_history = self.get_history_by_user_service()

        if title in user_history:
            print(user_history[title])
            user_history[title].append(time.time())
        else:
            user_history[title] = [time.time()]

        payload = {'email': utils.email_user, 'songs': user_history}
        utils.send_uri(method="PUT", payload=payload, endpoint='add-history')['message']