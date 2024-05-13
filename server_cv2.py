from flask import Flask, request
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive_image():
    # Obtener los datos de la imagen desde la solicitud POST
    image_data = request.data

    # Guardar los datos de la imagen en un archivo binario
    with open('imagen_original.raw', 'wb') as f:
        f.write(image_data)

    # Leer los datos de la imagen desde el archivo binario
    image_np = np.fromfile('imagen_original.raw', dtype=np.uint16)

    # Reorganizar los datos para que tengan la forma de la imagen original
    # Ajusta las dimensiones según el tamaño de tu imagen
    # Por ejemplo, para una imagen de 640x480:
    height, width, channels = 480, 640, 4
    if len(image_np) % (height * width * channels) == 0:
        num_images = len(image_np) // (height * width * channels)
        image_np = np.reshape(image_np, (num_images, height, width, channels))
    else:
        return 'Error: Tamaño del array no compatible con las dimensiones de la imagen.', 400

    # Convertir a formato compatible con OpenCV (BGR)
    image_cv = (image_np / 65535.0 * 255).astype(np.uint8)

    # Guardar la imagen en un archivo local
    cv2.imwrite('imagen_original.png', image_cv[0])  # Solo guardamos la primera imagen si hay varias

    return 'Imagen recibida y guardada correctamente.', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
