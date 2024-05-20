import cv2
import time

# Inicializa la captura de video desde la cámara (0 es la cámara predeterminada)
cap = cv2.VideoCapture(0)

# Verifica si la cámara se ha abierto correctamente
if not cap.isOpened():
    print("Error al abrir la cámara")
    exit()

# Define el delay en segundos
delay = 0.15  # por ejemplo, un delay de 2 segundos

while True:
    # Captura frame por frame
    ret, frame = cap.read()

    # Verifica si se ha capturado el frame correctamente
    if not ret:
        print("Error al capturar el frame")
        break

    # Muestra el frame en una ventana
    cv2.imshow('Frame', frame)

    # Introduce el delay
    time.sleep(delay)

    # Presiona 'q' en el teclado para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cuando todo esté listo, libera la captura y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
