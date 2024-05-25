import os, sys, cv2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

pixel = False
cap = cv2.VideoCapture(1) if pixel else cv2.VideoCapture(0)

marker_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
param_markers = cv2.aruco.DetectorParameters_create()

def procesar_frame(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, reject = cv2.aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)
    if corners:
        frame = utils.draw_marker_detected(frame=frame, marker_IDs=ids, marker_corners=corners)
    cv2.imshow("frame", frame)

while True:
    ret, frame = cap.read()
    procesar_frame(frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()