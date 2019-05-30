import numpy as np 
import cv2, pickle, json

# Setup JSON File #########################################################

try:
    jsonsets = json.loads(open('AllSets.json',encoding="utf8").read())
except MemoryError:
    raise Exception('Please ensure you are running 64 bit Python')
print('json file loaded')

# setup ORB Matching ###################################################

orb = cv2.ORB_create()

bf = cv2.BFMatcher(cv2.NORM_HAMMING)

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

# getSets returns list of all setcodes ################################

def getSets():
    #return alphabetized list of all sets, removing sets for which no card images exist
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

print(getSets())

