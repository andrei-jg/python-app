from kivy.lang import Builder
from kivy.utils import platform
from kivy_app import MyApp

angle = 0
resolution = "(1920, 1080)"
if platform == 'android':
    angle = -90

Builder.load_string(f'''
<MyLayout>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: {resolution}
        play: True
        canvas.before:
            PushMatrix
            Rotate:
                angle: {angle}
                origin: self.center
        canvas.after:
            PopMatrix
    ProcessedFrame:
        id: processed_frame
''')

if __name__ == "__main__":
    MyApp().run()