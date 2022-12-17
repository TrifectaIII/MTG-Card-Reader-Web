# Matching Package for https://github.com/TrifectaIII/MTG-Card-Reader-Web
# Handles the matching of webcam images to individual cards
# Uses opencv's ORB feature descriptor

from __future__ import annotations
import cv2
import numpy as np
from base64 import b64decode
import pickle
import json


class Match:

    def __init__(self, sfid: str, matchCount: int) -> None:
        self.sfid = sfid
        self.matchCount = matchCount

    @staticmethod
    def findBest(matches: list[Match]) -> Match | None:
        # find the best match from a list
        if (len(matches) == 0): return None
        bestMatch = matches[0]
        for match in matches[1:]:
            if match.matchCount > bestMatch.matchCount:
                bestMatch = match
        return bestMatch


class Identifier:

    def __init__(self) -> None:
        # creat required cv2 orb and brute force matcher objects
        self.orb = cv2.ORB_create()
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Counts Number of Good Matches using Ratio Test
    def ratioTestCount(self, des1, des2) -> int:
        good_matches = 0
        matches = self.matcher.knnMatch(des1, des2, k=2)
        for pair in matches:
            try:
                m, n = pair
                if m.distance < 0.75*n.distance:
                    good_matches += 1
            except ValueError:
                pass
        return good_matches

    # Matches image to a card
    def identify(self, img, setcode) -> Match | None:

        # Detect and Compute ORB Descriptors
        _, desCam = self.orb.detectAndCompute(img, None)

        # Read setDes Data from File if not loading all
        if not loadall:
            with open('setDes/set'+setcode+'.pkl', 'rb') as des_file:
                desDict = pickle.load(des_file)
        # Else retrieve setDes Data from dictionary
        else:
            global setsDict
            desDict = setsDict[setcode]

        # Find Match
        bestCount = 0
        bestSFID = ''

        for sfid in (list(desDict.keys())):
            desCard = desDict[sfid]
            matchCount = self.ratioTestCount(desCam, desCard)
            if matchCount > bestCount:
                bestCount = matchCount
                bestSFID = sfid

        #convert SFID into String
        bestSFID = str(bestSFID)

        # Build Dictionary to return and send to JS
        try:
            bestName = cardsInfo[bestSFID]
        except:
            bestName = ''

        card_dict = {
            'name':bestName,
            'sfid':bestSFID,
        }
        
        return card_dict


# Global Switch on Reading From Files vs Loading All to Memory
loadall = False
setsDict = dict()


#Load All SetDes files to Memory
def loadAllFiles():
    from os import walk
    setsGen = []
    for (dirpath, dirnames, filenames) in walk('setDes'):
        for fn in filenames:
            setsGen.append(fn[3:-4])#cuts off the leading 'set' and trailing '.des'
        break
    setsGen.sort()

    global setsDict
    for setcode in setsGen:
        with open('setDes/set'+setcode+'.pkl', 'rb') as des_file:
            desDict = pickle.load(des_file)
        setsDict[setcode] = desDict

    global loadall
    loadall = True