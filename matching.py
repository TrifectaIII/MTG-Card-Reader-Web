import cv2
import numpy as np
from base64 import b64decode
import pickle
from os import path, walk

# Setup ORB
orb = cv2.ORB_create()

# Create Brute Force Matcher Object
bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# Global Switch on Reading From Files vs Loading All to Memory
loadall = False

#Load All SetDes files to Memory
if loadall:
    setsGen = []
    for (dirpath, dirnames, filenames) in walk('resources/setDes'):
        for fn in filenames:
            setsGen.append(fn[:-4])
        break
    setsGen.sort()

    setsDict = dict()

    for setcode in setsGen:
        with open('resources/setDes/'+setcode+'.des', 'rb') as des_file:
            set_names, set_mvids, set_des = pickle.load(des_file)
        setsDict[setcode] = (set_names, set_mvids, set_des)


def uriToCv2(png_uri):
    # Converts URI PNG from AJAX to cv2 Image

    # Remove URI header from png data
    png_arr = png_uri.split(',')
    png_data = png_arr[1]
    # Decode base64 png data
    png_data_decode = b64decode(png_data)
    # Create numpy array with png data
    np_arr = np.asarray(bytearray(png_data_decode), dtype=np.uint8)
    # Convert numpy array to cv2 image, then return
    img_cv2 = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    return img_cv2


def ratioTestCount(matcher, des1, des2):
    # Counts Number of Good Matches using Ratio Test ()
    good_matches = 0
    matches = matcher.knnMatch(des1, des2, k=2)
    for pair in matches:
        try:
            m, n = pair
            if m.distance < 0.75*n.distance:
                good_matches += 1
        except ValueError:
            pass
    return good_matches


def match(cam_png_uri, setcode):
    # Matches URI PNG to Card

    global bf
    global orb
    global loadall

    # Convert request data to cv2 image
    img = uriToCv2(cam_png_uri)

    # Detect and Compute ORB Descriptors
    _, desCam = orb.detectAndCompute(img, None)

    # Read setDes Data from File if not loading all
    if not loadall:
        with open('resources/setDes/'+setcode+'.des', 'rb') as des_file:
            set_names, set_mvids, set_des = pickle.load(des_file)
    # Else retrieve setDes Data from dictionary
    else:
        global setsDict
        set_names, set_mvids, set_des = setsDict[setcode]

    # Find Match
    bestCount = 0
    bestName = ''
    bestMVID = ''

    for i in range(len(set_names)):
        name = set_names[i]
        mvid = set_mvids[i]
        des = set_des[i]
        matchCount = ratioTestCount(bf, desCam, des)
        if matchCount > bestCount:
            bestCount = matchCount
            bestName = name
            bestMVID = mvid

    # Return Name and URL for Matched Card
    return (bestName, bestMVID)


# def setsStr():
#     # Returns list of all stored setcodes
#     from os import walk
#     setsGen = []
#     for (dirpath, dirnames, filenames) in walk('resources/setDes'):
#         for fn in filenames:
#             setsGen.append(fn[:-4])
#         break
#     setsGen.sort()

#     # Access List of Set Names
#     with open('resources/sets.dict','rb') as dict_file:
#         setnameDict = pickle.load(dict_file)

#     # Generate String with setcodes and names of generated sets
#     # Sets seperated by ',' setcode and setname seperated by '#'
#     setsList = []
#     for setcode in setsGen:
#         setsList.append(setcode+'#'+setnameDict[setcode])

#     fstr = ','.join(setsList)

#     return fstr
