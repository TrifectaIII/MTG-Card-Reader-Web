import numpy as np
import cv2
import json
import pickle
from urllib import request as urlreq
from os import path

# Setup JSON File #####################################################

try:
    with open('resources/AllSets.json', encoding="utf8") as json_file:
        jsonsets = json.loads(json_file.read())
except MemoryError:
    raise Exception('Please ensure you are running 64 bit Python')
print('json file loaded')

# setup ORB  ##########################################################

orb = cv2.ORB_create()


setcode = 'CON'

if path.isfile('setDes/'+setcode+'.des'):
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
    with open('setDes/'+setcode+'.des', 'wb') as des_file:
        pickle.dump(setInfo, des_file)