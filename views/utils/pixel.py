import cv2

# Create a VideoCapture object for the webcam (0 is usually the default index for the first webcam)
imagen_cv = cv2.VideoCapture(1)

# Check if the webcam opened successfully
if not imagen_cv.isOpened():
    print("Error: Couldn't open webcam.")
    exit()

# Loop to capture frames from the webcam
while True:
    # Capture a frame from the webcam
    ret, frame = imagen_cv.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Couldn't capture frame.")
        break

    # Detect ArUco markers in the captured frame
    marker_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
    param_markers = cv2.aruco.DetectorParameters_create()
    marker_corners, marker_IDs, _ = cv2.aruco.detectMarkers(frame, marker_dict, parameters=param_markers)

    # Draw detected markers on the frame
    if marker_corners:
        cv2.aruco.drawDetectedMarkers(frame, marker_corners, marker_IDs)

    # Display the frame with detected markers
    cv2.imshow('Frame', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all OpenCV windows
imagen_cv.release()
cv2.destroyAllWindows()
