import numpy as np
import cv2
import pickle
import json
from urllib import request as urlreq
from os import path, rename

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
        if empties == 0:
            retsets.append(set)
        elif exists >= empties:
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

# Save each sets descriptors dict as file in setDes/ ########

for setcode in getSets():
    if path.isfile('setDes/set'+setcode+'.des'):
        # Skip if file exists
        print(setcode, 'file found, skipping')
    
    else:
        print('Starting', setcode)
        set_names = []
        set_mvids = []
        set_des = []
        try:
            # Get card objects from mtgjson
            cards = jsonsets[setcode]['cards']
        except:
            raise ValueError('No set found with that setcode')
        for card in cards:
            # For each card, save to dictionary
            name = card['name']
            try:
                mvid = card['multiverseId']
            except:
                #print(name,'has missing MVID')
                pass
            else:
                #print(name,'works')
                url = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+str(mvid)+'&type=card'
                url_response = urlreq.urlopen(url)
                img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
                img = cv2.imdecode(img_array, cv2.IMREAD_GRAYSCALE)
                _, des = orb.detectAndCompute(img, None)
                set_names.append(name)
                set_mvids.append(mvid)
                set_des.append(des)

        setInfo = (set_names, set_mvids, set_des)
        with open('setDes/set'+setcode+'.des', 'wb') as des_file:
            pickle.dump(setInfo, des_file)