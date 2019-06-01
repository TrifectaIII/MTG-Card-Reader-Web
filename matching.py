import cv2
import numpy as np
from base64 import b64decode
import pickle

#Setup ORB
orb = cv2.ORB_create()

#Create Brute Force Matcher Object
bf = cv2.BFMatcher(cv2.NORM_HAMMING)


def ratioTestCount(matcher,des1,des2):
    #Counts Number of Good Matches using Ratio Test ()
    good_matches = 0
    matches = matcher.knnMatch(des1,des2,k=2)
    for pair in matches:
        try:
            m,n = pair
            if m.distance < 0.75*n.distance:
                good_matches += 1
        except ValueError:
            pass
    return good_matches


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

def match(cam_png_uri,setcode):
    #Matches URI PNG to Card

    global bf
    global orb

    # Convert request data to cv2 image
    img = uriToCv2(cam_png_uri)

    # Detect and Compute ORB Descriptors
    _,desCam = orb.detectAndCompute(img,None)

    # Read setDes Data from File
    with open('resources/setDes/'+setcode+'.des','rb') as des_file:
        set_names,set_urls,set_des = pickle.load(des_file)

    # Find Match
    bestCount = 0
    bestName = ''
    bestURL = ''

    for i in range(len(set_names)):
        name = set_names[i]
        url  = set_urls[i]
        des  = set_des[i]
        matchCount = ratioTestCount(bf,desCam,des)
        if matchCount > bestCount:
            bestCount = matchCount
            bestName  = name
            bestURL   = url



    # PLACEHOLDER Display image and wait for key press
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return (bestName,bestURL)


