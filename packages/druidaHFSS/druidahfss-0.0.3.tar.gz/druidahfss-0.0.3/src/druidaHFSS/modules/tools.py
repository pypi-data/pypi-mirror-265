# import opencv
import cv2
import os
import numpy as np
import imutils  # https://pypi.org/project/imutils/


def cropImage(fullpath,image_path, image_name,output_path, resize_dim):
    # Read an image
    # input_image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    input_image = cv2.imread(fullpath, cv2.IMREAD_UNCHANGED)


    # Convert from BGR to HSV color space
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)

    # Get the saturation plane - all black/white/gray pixels are zero, and colored pixels are above zero.
    s = hsv[:, :, 1]

    #cv2.imshow('image', s) 
    # Apply threshold on s - use automatic threshold algorithm (use THRESH_OTSU).
    _, thresh = cv2.threshold(s, 10, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Find contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts) 

    # Find the contour with the maximum area.
    c = max(cnts, key=cv2.contourArea)

    # Get bounding rectangle
    x, y, w, h = cv2.boundingRect(c)

    # Crop the bounding rectangle out of img
    output_image = input_image[y:y+h, x:x+w, :].copy()

    dim = resize_dim
  
    # resize image
    output_image = cv2.resize(output_image, dim, interpolation = cv2.INTER_AREA)  

    # Save image
    isExist = os.path.exists(output_path +image_path)



    
    if not isExist:

        # Create a new directory because it does not exist
        os.makedirs(output_path + image_path)
        print("The new directory is created!")
    cv2.imwrite(output_path +image_path+image_name, output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return output_image