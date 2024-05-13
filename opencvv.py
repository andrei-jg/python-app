import cv2
import numpy as np

# define a video capture object 
vid = cv2.VideoCapture(1) 
  
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 

    marker_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
    param_markers = cv2.aruco.DetectorParameters_create()
    marker_corners, marker_IDs, _ = cv2.aruco.detectMarkers(frame, marker_dict, parameters=param_markers)

    if marker_corners:
        print("YEAAAAAA")
        for ids, corners in zip(marker_IDs, marker_corners):
            tamano_marcador_pixeles = max(np.linalg.norm(corners[0][0] - corners[0][1]),
                                            np.linalg.norm(corners[0][1] - corners[0][2]))
            tamano_real_marcador_cm = 5.0  # Modifica esto con el tamaño real de tu marcador
            tamano_real_marcador = (tamano_real_marcador_cm * tamano_marcador_pixeles) / tamano_marcador_pixeles
            org_x, org_y = int(corners[0][0][0]), int(corners[0][0][1])
            cv2.polylines(frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv2.LINE_AA)
            cv2.putText(frame, f'{tamano_real_marcador:.2f} cm', (org_x, org_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            # Dibujar el contorno del marcador
            cv2.drawContours(frame, [corners.astype(np.int32)], -1, (0, 255, 0), 2)
            # self.marker_size_label.text = f'Marker Size: {tamano_real_marcador:.2f} cm'
  
    # Display the resulting frame 
    cv2.imshow('frame', frame) 
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
