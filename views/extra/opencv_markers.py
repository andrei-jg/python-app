import os, sys, cv2, numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils, calibration_camera

pixel = utils.pixel
cap = cv2.VideoCapture(2) if pixel else cv2.VideoCapture(0)
device = "calibration_data_pixel" if pixel else "calibration_data_pc"

matrix, dist = utils.read_camera_calibration_params()
chord = "3,2,X,X,X,1"

def procesar_frame(frame: cv2.UMat):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, reject = cv2.aruco.detectMarkers(gray_frame, utils.aruco_dict, parameters=utils.parameters)
    if corners:
        pass
        frame = utils.draw_marker_detected(frame=frame, marker_IDs=ids, marker_corners=corners, 
                                                coefficients_matrix=matrix, distortion_coefficients=dist, chord=chord)
      
    # calibration_camera.process_image(frame)
    cv2.imshow("frame", frame)

while True:
    ret, frame = cap.read()
    # cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE), 0
    procesar_frame(frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()