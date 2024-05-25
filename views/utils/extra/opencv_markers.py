import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
marker_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_1000)
param_markers = cv.aruco.DetectorParameters_create()

def procesar_frame(frame):

    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    corners, ids, reject = cv.aruco.detectMarkers(gray_frame, marker_dict, parameters=param_markers)

    if corners:
        cv.aruco.drawDetectedMarkers(frame, corners, ids)


    cv.imshow("frame", frame)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    procesar_frame(frame)

    key = cv.waitKey(1)
    if key == ord("q"):
        break

cap.release()
cv.destroyAllWindows()