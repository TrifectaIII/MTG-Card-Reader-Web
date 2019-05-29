import cv2
import numpy as np
from base64 import b64decode

#Setup ORB
orb = cv2.ORB_create()

#Create Brute Force Matcher Object
bf = cv2.BFMatcher(cv2.NORM_HAMMING)

#Create FLANN Matcher Object
# index_params= dict(algorithm = 6, #Algorithm 6 is FLANN_INDEX_LSH
#                    table_number = 6, # 12
#                    key_size = 12,     # 20
#                    multi_probe_level = 1) #2
# search_params = dict(checks=50)
# flann = cv2.FlannBasedMatcher(index_params,search_params)


def ratioTestCount(matcher,des1,des2):
    #Counts Number of Good Matches using Ratio Test ()
    good_matches = []
    matches = matcher.knnMatch(des1,des2,k=2)
    for pair in matches:
        try:
            m,n = pair
            if m.distance < 0.75*n.distance:
                good_matches.append(m)
        except ValueError:
            pass
    return len(good_matches)


def uriToCv2(png_uri):
    #Converts URI PNG from AJAX to cv2 Image

    # Remove URL header from png data
    png_arr = png_uri.split(b',')
    png_data = png_arr[1]
    # Decode base64 png data
    png_data_decode = b64decode(png_data)
    # Create numpy array with png data
    np_arr = np.asarray(bytearray(png_data_decode), dtype=np.uint8)
    # Convert numpy array to cv2 image, then return
    img_cv2 = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img_cv2

def match(cam_png_uri):
    #Matches URI PNG to Card

    global bf
    global orb
    #global flann

    # Convert request data to cv2 image
    img = uriToCv2(cam_png_uri)

    #Detect and Compute ORB Descriptors
    kp,des = orb.detectAndCompute(img,None)

    # Display image and wait for key press
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return "match function still a WIP"
