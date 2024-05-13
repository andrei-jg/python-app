import cv2
import time

def mostrar_video_camara():
    # Abre la cámara web (puedes cambiar el número 0 por otro si tienes múltiples cámaras)
    cap = cv2.VideoCapture(0)

    while True:
        # Captura fotograma por fotograma
        ret, frame = cap.read()

        # Muestra el fotograma en una ventana
        cv2.imshow('Video de la cámara', frame)

        time.sleep(0.2)

        # Espera 1 milisegundo y verifica si se ha presionado la tecla 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera la captura y cierra la ventana
    cap.release()
    cv2.destroyAllWindows()

# Llama a la función para mostrar el video de la cámara
mostrar_video_camara()
