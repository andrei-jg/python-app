import cv2

# Ruta de la imagen
ruta_imagen = 'imagen_request.jpg'

while True:
    # Cargar la imagen

    try:

        imagen = cv2.imread(ruta_imagen)

        # Mostrar la imagen
        cv2.imshow('Imagen', imagen)

    except:
        pass

    # Esperar un momento y detectar si se presiona la tecla 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos y cerrar todas las ventanas
cv2.destroyAllWindows()
