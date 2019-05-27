import cv2
import numpy as np
from base64 import b64decode

def uriToCv2(png_uri):
    
    # Remove URL header from png data
    png_arr = png_uri.split(b',')
    png_data = png_arr[1]
    
    #Decode base64 png data
    png_data_decode = b64decode(png_data)
    
    #Create numpy array with png data
    np_arr = np.asarray(bytearray(png_data_decode), dtype=np.uint8)
    
    #Convert numpy array to cv2 image, then return
    img_cv2 = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img_cv2

def match(cam_png_uri):

    # Convert request data to cv2 image
    img = uriToCv2(cam_png_uri)
    
    # Display image and wait for key press
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return "match function still a WIP"