import cv2
import numpy as np

# Ruta de la imagen
image_path = "images/res_original.png"

# Cargar la imagen con OpenCV
image = cv2.imread(image_path)

# Convertir la imagen en un array numpy utilizando np.frombuffer
frame_data = image.tobytes()
nparr = np.frombuffer(frame_data, dtype=np.uint8)

# Reorganizar el array para tener la forma correcta (altura, anchura, canales)
frame_np = nparr.reshape((image.shape[0], image.shape[1], 3))  # Assumiendo que la imagen es en formato BGR

# Convertir la imagen de BGR a RGB (si es necesario)
# frame_rgb = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)

# Puedes seguir trabajando con frame_np como lo harías con frame_np en tu código original.


# Visualizar la imagen usando OpenCV
cv2.imshow("Imagenn", image)
cv2.imshow("Imagen", nparr)

cv2.waitKey(0)
cv2.destroyAllWindows()
# Ahora puedes usar nparr en lugar de frame_data en tu código
