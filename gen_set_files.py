from typing import List
import numpy as np
import cv2
import pickle
import requests
import os
import time
import MtgJsonUtil


# change working directory to directory of file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def getCvImageBySFID(sfid):
    # Function for getting cv2 image with sfid using scryfall api

    # scryfall api request formatting: only needs sfid
    url = 'https://api.scryfall.com/cards/{}/?format=image&version=border_crop'.format(str(sfid))

    # make request
    try:
        r = requests.get(url)
    except:
        r = None

    # tracks the backoff
    backoffLevel: int = 0

    # continue to retry with exponential backoff, if failed
    while not r or r.status_code != 200:
        backoffLevel += 1
        backoffMinutes = backoffLevel ** backoffLevel
        print("Will retry after " + str(backoffMinutes) + " minutes... SFID: " + str(sfid))
        time.sleep(60 * backoffMinutes)
        try:
            r = requests.get(url, timeout=20)
        except:
            r = None

    # process image when request successful
    np_array = np.frombuffer(r.content, np.uint8)
    img_np = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
    return img_np


# Save each sets descriptors dict as file in setDes/ ##########

# setup ORB  
orb = cv2.ORB_create()

# get data from mtgjson
setsList: List[str] = list(MtgJsonUtil.getSetsWithSfids().keys())
jsonData: dict = MtgJsonUtil.parseMtgJson()

# WARNING: FOR DELETING ALL OLD FILES
# for setcode in getSets():
#     if path.isfile('setDes/set'+setcode+'.pkl'):
#         remove('setDes/set'+setcode+'.pkl')

# loop through each set
for setcode in setsList:
    # SKIP IF FILE EXISTS
    if os.path.isfile('setDes/set'+setcode+'.pkl'):
        print(setcode, 'file found, skipping')
        pass
    else:
        print(setcode, '--------------------------------------')
        set_sfids = []
        set_des = []
        try:
            # Get card objects from mtgjson
            cards = jsonData[setcode]['cards']
        except:
            raise Exception('No set found with setcode: ' + setcode)
        for card in cards:
            # For each card, save to dictionary
            try:
                sfid = card['identifiers']['scryfallId']
                print(setcode, card['name'], card['identifiers']['scryfallId'])
            except:
                pass
            else:
                #time delay to avoid overloading scryfall api
                time.sleep(0.25)
                img = getCvImageBySFID(sfid)

                _, des = orb.detectAndCompute(img, None)
                set_sfids.append(sfid)
                set_des.append(des)

        #generate new file
        setInfo = dict()

        for i in range(len(set_sfids)):
            setInfo[set_sfids[i]] = set_des[i]

        with open('setDes/set'+setcode+'.pkl', 'wb') as des_file:
            pickle.dump(setInfo, des_file)
