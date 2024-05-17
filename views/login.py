from kivy.lang import Builder
from kivymd.app import MDApp
from new_login import MainApp


kv = """
Screen:
    MDCard:
        size_hint: 0.9, None  # Adjust the width relative to the screen size
        height: self.minimum_height  # Automatically adjust the height according to the content
        pos_hint: {'center_x': 0.5, 'center_y': 0.55}
        elevation: 10
        padding: '10dp'  # Use dp to ensure a consistent size across different resolutions
        spacing: '10dp'
        orientation: 'vertical'

        Image:
            source: 'views/images/vrLogo.png'
            size_hint: None, None
            size: '170dp', '170dp'  # Adjust size as needed
            pos_hint: {'center_x': 0.5}

        MDLabel:
            id: welcome_label
            text: 'SIRMG'
            font_size: '32sp'  # Use sp for font size for scalability
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: '-3dp'
            bold: True

        MDLabel:
            
            text: "Clásica"
            halign: 'right'  # Alinea el texto horizontalmente al centro
            size_hint_y: None  # Fuerza al MDLabel a tener una altura específica
            size_hint_x: 0.7
            height: self.texture_size[1]  # Ajusta la altura basándose en el tamaño del texto
            paddig_x: '10dp'
            padding_y: '-3dp'  # Ajusta el espacio vertical entre la imagen y el texto

        Widget:
            size_hint_y: None
            height: '10dp'  # Spacer adjusted to a relative size

        MDTextField:
            mode: 'round'
            id: user
            hint_text: 'Correo'
            icon_right: 'account'
            size_hint: 0.95, None  # Adjust the size relatively
            height: '48dp'
            font_size: '16sp'
            pos_hint: {'center_x': 0.5}

        Widget:
            size_hint_y: None
            height: '10dp'  # Spacer adjusted to a relative size

        MDTextField:
            mode: 'round'
            id: password
            hint_text: 'Contraseña'
            icon_right: 'eye-off'
            size_hint: 0.95, None  # Adjust the size relatively
            height: '48dp'
            font_size: '16sp'
            pos_hint: {'center_x': 0.5}
            password: True

        Widget:
            size_hint_y: None
            height: '20dp'  # Spacer adjusted to a relative size

        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height
            size_hint_x: 1.05
            spacing: '10dp'
            pos_hint: {'center_x': 0.5}
            padding: '10dp'
            orientation: 'horizontal'

            MDRoundFlatButton:
                text: 'Iniciar Sesión'
                font_size: '14sp'
                size_hint: 0.3, None  # Adjust the size relatively
                size_hint_y: None  # Use size_hint_y to allow height scaling
                height: '48dp'
                on_press: app.switch()

            MDRoundFlatButton:
                text: 'Olvidé mi cuenta'
                font_size: '14sp'
                size_hint: 0.3, None  # Adjust the size relatively
                size_hint_y: None  # Use size_hint_y to allow height scaling
                height: '48dp'
"""

class MainAppLogin(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_string(kv)
    
    def switch(self):
        MainApp().run()


MainAppLogin().run()
