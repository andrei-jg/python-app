import cv2, pickle, glob, numpy as np

# Configuration parameters
chessboard_size = (5, 7)
frame_size = (1920, 1280)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 3D object points
object_points = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
object_points[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# Lists to store 3D points and image points from all images
objpoints = []
imgpoints = []

global images_processed
images_processed = 0

def process_image(frame):
    global images_processed
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    if ret:
        # print(image_file)
        objpoints.append(object_points)
        refined_corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(refined_corners)
        images_processed = images_processed + 1
        print(images_processed)

    if images_processed > 50:
        calibrate_camera()

# def calibrate_camera(image_dir='images/*.png'):
def calibrate_camera():    

    """Calibrate the camera using chessboard images."""
    # Calibrate the camera
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints,
        imgpoints,
        frame_size,
        None,
        None
    )

    if not ret:
        raise RuntimeError("Camera calibration failed.")
    
    calibration_data = {
        'camera_matrix': camera_matrix,
        'dist_coeffs': dist_coeffs,
    }

    # Guarda el diccionario en un archivo usando pickle
    with open('calibration_data.pkl', 'wb') as archivo:
        pickle.dump(calibration_data, archivo)

    # print("Camera matrix:\n", camera_matrix)
    # print("Distortion coefficients:\n", dist_coeffs)
    print("Datos guardados en calibration_data.pkl")

    exit()