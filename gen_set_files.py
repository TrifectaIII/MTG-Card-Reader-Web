import numpy as np 
import cv2, pickle, json
from urllib import request as urlreq
from os import path

# Setup JSON File #####################################################

try:
    jsonsets = json.loads(open('resources/AllSets.json',encoding="utf8").read())
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
        empties = False
        exists = False
        multiverse_ids = []
        for card in cards:
            try:
                multiverse_ids.append(card['multiverseId'])
                exists = True
            except:
                multiverse_ids.append(None)
                empties = True
        if (empties and (not exists)):
            pass
        elif (empties and exists):
            pass
        else:
            retsets.append(set)
    retsets = sorted(retsets)
    return retsets

def getSetsStr():
    #Joins all setcodes by commas
    return ','.join(getSets())

# Save sets string as file ############################################

with open('resources/sets.txt','w') as text_file:
    text_file.write(getSetsStr())

# Save each sets descriptors dict as file in resources/setDes/ ########

#for setcode in getSets():
for setcode in ['5ED']:
    if path.isfile('resources/setDes/'+setcode+'.des'):
        print(setcode,'file found, skipping')
    else:
        print('Starting',setcode)
        set_names = []
        set_urls  = []
        set_des   = []
        try:
            #Get card objects from mtgjson
            cards = jsonsets[setcode]['cards']
        except:
            raise ValueError('No set found with that setcode')
        for card in cards:
            #For each card, save to dictionary
            name = card['name']
            id = card['multiverseId']
            url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+str(id)+'&type=card'
            print(name,url)
            url_response = urlreq.urlopen(url)
            img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, -1)
            _,des = orb.detectAndCompute(img,None)
            set_names.append(name)
            set_urls.append(url)
            set_des.append(des)

        setInfo = (set_names,set_urls,set_des)
        with open('resources/setDes/'+setcode+'.des','wb') as des_file:
            pickle.dump(setInfo,des_file)