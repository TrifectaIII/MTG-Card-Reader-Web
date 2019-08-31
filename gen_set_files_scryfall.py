# Script that processes images from Scryfall API for use with https://github.com/TrifectaIII/MTG-Card-Reader-Web
# Uses opencv's ORB feature descriptor

import numpy as np
import cv2
import pickle
import json
from urllib import request as urlreq
from os import path, rename, remove
import numpy as np
import time


# Setup JSON File #####################################################

try:
    with open('resources/AllSets.json', encoding="utf8") as json_file:
        jsonsets = json.loads(json_file.read())
except MemoryError:
    raise Exception('Please ensure you are running 64 bit Python')
print('json file loaded')


# setup ORB  ##########################################################

orb = cv2.ORB_create()


# getSets returns list of all setcodes ################################

def getSets():
    # return alphabetized list of all sets,
    # removing sets for which no card images exist
    retsets = []
    for set in (list(jsonsets.keys())):
        cards = jsonsets[set]['cards']
        empties = 0
        exists = 0
        multiverse_ids = []
        for card in cards:
            try:
                multiverse_ids.append(card['multiverseId'])
                exists += 1
            except:
                multiverse_ids.append(None)
                empties += 1
        if empties == 0 and exists > 0:
            retsets.append(set)
        elif exists > 0:
            retsets.append(set)
    retsets = sorted(retsets)
    return retsets


def getSetsDict():
    # Joins all setcodes by commas
    #return ','.join(getSets())
    setsdict = dict()
    for set in getSets():
        setsdict[set] = jsonsets[set]['name']
    return setsdict


# Save sets dict as file ##############################################

with open('static/sets.json','w') as dict_file:
    json.dump(getSetsDict(),dict_file)


# Save dictionary of all mvids ########################################

mvidDict = dict()

total = 0

for set in (list(jsonsets.keys())):
    cards = jsonsets[set]['cards']
    for card in cards:
        try:
            mvid = card['multiverseId']
            name = card['name']
            number = card['number']
            purchaseUrls = card['purchaseUrls']
        except:
            pass
        else:
            total += 1
            mvidDict[mvid] = {'name':name, 'number':number, 'purchaseUrls':purchaseUrls}

with open('static/cardsInfo.json','w') as jsonfile:
    json.dump(mvidDict,jsonfile)


# Function for getting cv2 image with mvid using scryfall api #########

def getCvImageByMVID(mvid):
    # scryfall api request formatting: only needs mvid as show 
    # https://api.scryfall.com/cards/multiverse/409574/?format=image&version=border_crop
    response = urlreq.urlopen('https://api.scryfall.com/cards/multiverse/{}/?format=image&version=border_crop'.format(str(mvid)))
    nparr = np.frombuffer(response.read(), np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np


# Save each sets descriptors dict as file in setDesScryfall/ ##########

# WARNING: FOR DELETING MANY FILES AT ONCE
# for setcode in getSets():
#     if path.isfile('setDesScryfall/set'+setcode+'.pkl'):
#         remove('setDesScryfall/set'+setcode+'.pkl')

for setcode in getSets():
    # SKIP IF FILE EXISTS
    if path.isfile('setDesScryfall/set'+setcode+'.pkl'):
        print(setcode, 'file found, skipping')
        pass
    else:
        # FOR CONVERTING OLD FILES TO NEW NAMING SCHEME
        # if path.isfile('setDesScryfall/set'+setcode+'.des'):
        #     print('converting old version of',setcode)
        #     with open('setDesScryfall/set'+setcode+'.des','rb') as oldfile:
        #         set_names, set_mvids, set_des = pickle.load(oldfile)
        # else:
        print('Starting', setcode)
        set_mvids = []
        set_des = []
        try:
            # Get card objects from mtgjson
            cards = jsonsets[setcode]['cards']
        except:
            raise ValueError('No set found with that setcode')
        for card in cards:
            # For each card, save to dictionary
            try:
                mvid = card['multiverseId']
                print(card['name'])
            except:
                pass
            else:
                #time delay to avoid overloading scryfall api
                time.sleep(0.5)
                img = getCvImageByMVID(mvid)

                _, des = orb.detectAndCompute(img, None)
                set_mvids.append(mvid)
                set_des.append(des)

        #Whether or not file can be converted from old, generate new file under current naming scheme
        setInfo = dict()

        for i in range(len(set_mvids)):
            setInfo[set_mvids[i]] = set_des[i]

        with open('setDesScryfall/set'+setcode+'.pkl', 'wb') as des_file:
            pickle.dump(setInfo, des_file)