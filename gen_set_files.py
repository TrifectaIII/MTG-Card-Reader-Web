# Script that processes images from Scryfall API for use with https://github.com/TrifectaIII/MTG-Card-Reader-Web
# Uses opencv's ORB feature descriptor

import numpy as np
import cv2
import pickle
import json
import requests
from os import path, chdir, remove
import numpy as np
import time

# change working directory to directory of file
abspath = path.abspath(__file__)
dname = path.dirname(abspath)
chdir(dname)

# Fetch JSON File from MTGJSON ########################################

def getMtgJson() -> bytes:

    print("Fetching MTGJSON File")

    # url for MTGJSONv5 API
    url = 'https://mtgjson.com/api/v5/AllPrintings.json'

    # need user agent header to avoid 403
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    # send request and recieve response
    r = requests.get(url, headers=headers)

    # make sure response was successful
    if r.status_code == 200:
        return r.content
    else:
        raise Exception("Could not get MTGJSON File, STATUS CODE: " + str(r.status_code))

# Download JSON File from MTGJSON ########################################

def downloadMtgJson() -> None:

    print("Downloading MTGJSON File")

    with open('resources/AllPrintings.json', 'wb') as json_file:
        json_file.write(getMtgJson())

# Setup JSON File #####################################################

try:
    with open('resources/AllPrintings.json', encoding="utf8") as json_file:
        # all sets in data space for MTGJSONv5
        jsonsets = json.loads(json_file.read())['data']
except MemoryError:
    raise Exception('Please ensure you are running 64 bit Python')
print('MTGJSON File Loaded')


# getSets returns list of all setcodes ################################

def getSets():
    # return alphabetized list of all sets,
    # removing sets for which no card images exist
    retsets = []
    for setCode in (list(jsonsets.keys())):
        cards = jsonsets[setCode]['cards']
        empties = 0
        exists = 0
        scryfall_ids = []
        for card in cards:
            try:
                scryfall_ids.append(card['identifiers']['scryfallId'])
                exists += 1
            except:
                scryfall_ids.append(None)
                empties += 1
        if empties == 0 and exists > 0:
            retsets.append(setCode)
        elif exists > 0:
            retsets.append(setCode)
    retsets = sorted(retsets)
    return retsets


def getSetsDict():
    # creates dict where setcodes are keys and names are values
    setsdict = dict()
    for setCode in getSets():
        setsdict[setCode] = jsonsets[setCode]['name']
    return setsdict


# Save sets dict as file ##############################################

with open('static/sets.json','w') as dict_file:
    json.dump(getSetsDict(),dict_file)


# Save dictionary of all sfids ########################################

sfidDict = dict()

total = 0

for set in (list(jsonsets.keys())):
    cards = jsonsets[set]['cards']
    for card in cards:
        try:
            sfid = card['identifiers']['scryfallId']
            name = card['name']
        except:
            pass
        else:
            total += 1
            sfidDict[sfid] = name

with open('resources/cardsInfo.json','w') as jsonfile:
    json.dump(sfidDict,jsonfile)


# Function for getting cv2 image with sfid using scryfall api #########

def getCvImageBySFID(sfid):
    # scryfall api request formatting: only needs sfid
    r = requests.get('https://api.scryfall.com/cards/{}/?format=image&version=border_crop'.format(str(sfid)))
    
    # process image if request successful
    if r.status_code == 200:
        np_array = np.frombuffer(r.content, np.uint8)
        img_np = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
        return img_np
    #otherwise throw an error
    else:
        raise Exception('Could not fetch card '+sfid+' image, STAUS CODE: '+str(r.status_code))


# Save each sets descriptors dict as file in setDes/ ##########

# WARNING: FOR DELETING ALL OLD FILES
# for setcode in getSets():
#     if path.isfile('setDes/set'+setcode+'.pkl'):
#         remove('setDes/set'+setcode+'.pkl')

# setup ORB  
orb = cv2.ORB_create()

for setcode in getSets():
    # SKIP IF FILE EXISTS
    if path.isfile('setDes/set'+setcode+'.pkl'):
        print(setcode, 'file found, skipping')
        pass
    else:
        print(setcode, '--------------------------------------')
        set_sfids = []
        set_des = []
        try:
            # Get card objects from mtgjson
            cards = jsonsets[setcode]['cards']
        except:
            raise Exception('No set found with setcode: ' + setcode)
        for card in cards[:5]:
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