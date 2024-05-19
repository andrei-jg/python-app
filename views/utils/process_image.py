from kivy.uix.widget import Widget
import numpy as np
import cv2, time

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_1000)
parameters = cv2.aruco.DetectorParameters_create()

def detect_markers(camera):
            
    '''
    Function to capture the images and give them the names
    according to their captured time and date.
    '''
    # file_name = self.get_path()

    # print("camera.texture: ",
    #         camera.texture.width,
    #         camera.texture.height
    #         )

    ### 1. Image - Con calidad ###            

    image_from_camera = Widget.export_as_image(camera)
    # img = Image(image_from_camera)
    # img.save(f'{file_name}original_.png')


    height, width = image_from_camera.texture.height, image_from_camera.texture.width
    # print(height, width)
    # 690 1000
    
    time_init = time.time()
    newvalue = np.frombuffer(image_from_camera.texture.pixels, np.uint8)
    newvalue = newvalue.reshape(height, width, 4)
    gray = cv2.cvtColor(newvalue, cv2.COLOR_RGBA2GRAY)
    print("newvalue: ", time.time() - time_init)

    time_init = time.time()
    
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print("aruco_dict: ", time.time() - time_init)

    if corners:
        print("Marker Detected")

        time_init = time.time()
        cv2.aruco.drawDetectedMarkers(gray, corners, ids)
        backtorgb = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
        print("backtorgb: ", time.time() - time_init)
        # cv2.imwrite(file_name, backtorgb)

