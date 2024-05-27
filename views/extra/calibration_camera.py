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

def process_image(image_file):
    """Process a single image for chessboard corners."""
    image = cv2.imread(image_file)
    if image is None:
        print(f"Error reading image {image_file}")
        return False

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    if ret:
        print(image_file)
        objpoints.append(object_points)
        refined_corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(refined_corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(image, chessboard_size, refined_corners, ret)
        cv2.imshow("Chessboard Corners", image)

        if cv2.waitKey(1) == ord("q"):
            return True
    return False

def calibrate_camera(image_dir='images/*.png'):
    """Calibrate the camera using chessboard images."""
    images = glob.glob(image_dir)
    for image_file in images:
        if process_image(image_file):
            break

    cv2.destroyAllWindows()

    if not objpoints or not imgpoints:
        raise ValueError("No corners found in any image. Calibration failed.")

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

    return camera_matrix, dist_coeffs

if __name__ == "__main__":
    try:
        camera_matrix, dist_coeffs = calibrate_camera()
        calibration_data = {
            'camera_matrix': camera_matrix,
            'dist_coeffs': dist_coeffs,
        }

        # Guarda el diccionario en un archivo usando pickle
        with open('calibration_data_pixel.pkl', 'wb') as archivo:
            pickle.dump(calibration_data, archivo)

        # print("Camera matrix:\n", camera_matrix)
        # print("Distortion coefficients:\n", dist_coeffs)
        print("Datos guardados en calibration_data.pkl")
    except Exception as e:
        print(f"An error occurred: {e}")