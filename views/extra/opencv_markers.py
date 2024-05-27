import os, sys, cv2, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

pixel = True
cap = cv2.VideoCapture(2) if pixel else cv2.VideoCapture(0)

matrix, dist = utils.read_camera_calibration_params()

marker_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
param_markers = cv2.aruco.DetectorParameters_create()

def procesar_frame(frame: cv2.UMat):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, reject = cv2.aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)
    if corners:
        time_init = time.time()
        # frame = utils.draw_marker_detected(frame=frame, marker_IDs=ids, marker_corners=corners, 
                                                # coefficients_matrix=matrix, distortion_coefficients=dist)

    cv2.imshow("frame", frame)

while True:
    ret, frame = cap.read()
    procesar_frame(frame)

    if cv2.waitKey(1) == ord("q"):
        break

    if cv2.waitKey(1) == ord("s"):
        cv2.imwrite(f'images/{utils.get_path()}', frame)

cap.release()
cv2.destroyAllWindows()