# Matching Package for https://github.com/TrifectaIII/MTG-Card-Reader-Web
# Handles the matching of webcam images to individual cards
# Uses opencv's ORB feature descriptor

import cv2
import numpy as np
from base64 import b64decode
import pickle
import json
import random
from tqdm import tqdm
from pool import pool, ratioTestCount, cloud_func
from multiprocessing import cpu_count
import pickle, base64
import requests
import faiss

# Load MVID Dictionary
with open("static/cardsInfo.json", "r") as mvidfile:
    cardsInfo = json.load(mvidfile)

# Setup ORB
orb = cv2.ORB_create()

# Create Brute Force Matcher Object

# Global Switch on Reading From Files vs Loading All to Memory
loadall = False
setsDict = dict()

# Load All SetDes files to Memory
def loadAllFiles():
    from os import walk

    setsGen = []
    for (dirpath, dirnames, filenames) in walk("setDes/"):
        for fn in filenames:
            setsGen.append(fn[3:-4])  # cuts off the leading 'set' and trailing '.des'
        break
    setsGen.sort()

    global setsDict
    for setcode in setsGen:
        with open("setDes/set" + setcode + ".pkl", "rb") as des_file:
            desDict = pickle.load(des_file)
        setsDict[setcode] = {k:v.astype(np.float32) for k,v in desDict.items()}

    global loadall
    loadall = True


def uriToCv2(img_uri):
    # Converts URI PNG/JPG from AJAX to cv2 Image

    # Remove URI header from png data
    img_arr = img_uri.split(",")
    img_data = img_arr[1]
    # Decode base64 png/jpg data
    img_data_decode = b64decode(img_data)
    # Create numpy array with png/jpg data
    np_arr = np.asarray(bytearray(img_data_decode), dtype=np.uint8)
    # Convert numpy array to cv2 image, then return
    img_cv2 = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    return img_cv2


# def ratioTestCount(des1, des2, mvid):
#     matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
#     # Counts Number of Good Matches using Ratio Test ()
#     good_matches = 0
#     matches = matcher.knnMatch(des1, des2, k=2)
#     for pair in matches:
#         try:
#             m, n = pair
#             if m.distance < 0.75*n.distance:
#                 good_matches += 1
#         except ValueError:
#             pass
#     return good_matches, mvid


def identify(cam_png_uri, setcode):
    # Matches URI PNG to Card
    global orb
    global loadall
    global cardsInfo
    index = faiss.IndexFlatL2(32)
    # Convert request data to cv2 image
    img = uriToCv2(cam_png_uri)
    # Detect and Compute ORB Descriptors
    _, desCam = orb.detectAndCompute(img, None)

    # Read setDes Data from File if not loading all
    if not loadall:
        with open("setDes/set" + setcode + ".pkl", "rb") as des_file:
            desDict = pickle.load(des_file)
    # Else retrieve setDes Data from dictionary
    else:
        global setsDict
        desDict = setsDict[setcode]

    # Find Match
    bestCount = 0
    bestMVID = ""
    randSets = list(setsDict.values())
    random.shuffle(randSets)
    results = []
    desCam = desCam.astype(np.float32)
    # index.train(desCam)
    # index.add(desCam)
    # chunk_len = int(len(randSets) / cpu_count()) + 1
    # chunks = [randSets[x: x + chunk_len] for x in range(0, len(randSets), chunk_len)]

    # ####TRUTH######
    for desDict in tqdm(randSets):
        for i, ln in enumerate(desDict.items()):
            mvid, des2 = ln
            index.add(des2)
    d, i = index.search(desCam, 2)
    

    # results.append(pool.apply_async(ratioTestCount, (desCam, desDict)))
    # for desDict in randSets:
    #     for mvid, des2 in desDict.items():
    #         # breakpoint()
    #         results.append(pool.apply_async(cloud_func, (desCam, des2, mvid)))

    # with open('all-sets-orb.pkl', 'rb') as f:
    #     desDict = dict(pickle.load(f))
    # results.append(pool.apply_async(ratioTestCount, (desCam, desDict)))
    # ratioTestCount(desCam, desDict)
    # print(results[-1])
    breakpoint()
    for res in tqdm(results):
        r = res.get()
        matchCount, mvid = r
        if matchCount > bestCount:
            print(matchCount, mvid, cardsInfo.get(bestMVID, {"name": ""})["name"])
            bestCount = matchCount
            bestMVID = mvid

    # convert MVID into String
    bestMVID = str(bestMVID)
    # Build Dictionary to return and send to JS
    try:
        bestName = cardsInfo[bestMVID]["name"]
    except:
        bestName = ""

    try:
        bestPurchase = cardsInfo[bestMVID]["purchaseUrls"]
    except:
        bestPurchase = ""

    card_dict = {"name": bestName, "mvid": bestMVID, "purchaseUrls": bestPurchase}

    return card_dict
