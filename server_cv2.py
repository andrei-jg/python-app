from flask import Flask, request, jsonify
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/convertir_a_pixels', methods=['POST'])
def convertir_a_pixels():

    # Obtener los datos de la imagen enviada en la solicitud POST
    imagen_data = request.data
    # Decodificar los datos de la imagen en formato numpy array
    imagen_np = np.frombuffer(imagen_data, np.uint8)
    # Decodificar el numpy array en una imagen OpenCV
    imagen_cv = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)

    cv2.imwrite('imagen_request.jpg', imagen_cv)

    # Aquí puedes realizar cualquier procesamiento de imagen que desees

    marker_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
    param_markers = cv2.aruco.DetectorParameters_create()
    marker_corners, marker_IDs, _ = cv2.aruco.detectMarkers(imagen_cv, marker_dict, parameters=param_markers)

    print(marker_dict)
    print(param_markers)
    print(marker_corners)

    if marker_corners:
        print("YEAAAAAA")
        for ids, corners in zip(marker_IDs, marker_corners):
            tamano_marcador_pixeles = max(np.linalg.norm(corners[0][0] - corners[0][1]),
                                            np.linalg.norm(corners[0][1] - corners[0][2]))
            tamano_real_marcador_cm = 5.0  # Modifica esto con el tamaño real de tu marcador
            tamano_real_marcador = (tamano_real_marcador_cm * tamano_marcador_pixeles) / tamano_marcador_pixeles
            org_x, org_y = int(corners[0][0][0]), int(corners[0][0][1])
            cv2.polylines(imagen_cv, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv2.LINE_AA)
            cv2.putText(imagen_cv, f'{tamano_real_marcador:.2f} cm', (org_x, org_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # Dibujar el contorno del marcador
            cv2.drawContours(imagen_cv, [corners.astype(np.int32)], -1, (0, 255, 0), 2)
            # self.marker_size_label.text = f'Marker Size: {tamano_real_marcador:.2f} cm'
        

    imagen_cv = cv2.cvtColor(imagen_cv, cv2.COLOR_RGBA2RGB)

    cv2.imwrite('imagen_processed.jpg', imagen_cv)

    # Convertir la imagen procesada de nuevo a formato JPEG
    _, jpeg_imagen = cv2.imencode('.jpg', imagen_cv)

    # Devolver la imagen procesada como respuesta
    return jpeg_imagen.tobytes(), 200, {'Content-Type': 'image/jpeg'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
