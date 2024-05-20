import cv2
import time

# Ruta de la imagen
ruta_imagen = 'IMG.png'

while True:
    # Cargar la imagen

    try:

        time_init = time.time()

        imagen = cv2.imread(ruta_imagen)
        cv2.imshow('Imagen', imagen)

        print("Total time: ", time.time() - time_init)

    except:
        pass

    # Esperar un momento y detectar si se presiona la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos y cerrar todas las ventanas
cv2.destroyAllWindows()