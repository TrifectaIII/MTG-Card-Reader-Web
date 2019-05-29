import numpy as np 
import cv2
from os import walk

from matplotlib import pyplot as plt

# Test the Matching Ability of ORB (Oriented FAST Rotated BRIEF)

#Setup ORB

orb = cv2.ORB_create()

# Load all Cam Images for Testing
test_imgs_names = []
for (dirpath, dirnames, filenames) in walk('./resources/test_cam/'):
    test_imgs_names.extend(filenames)
    break

test_imgs = []

for name in test_imgs_names:
    path = './resources/test_cam/' + name
    img = cv2.imread(path,0)
    kp, des = orb.detectAndCompute(img,None)
    test_imgs.append({'name':name,
                      'img':img,
                      'kp':kp,
                      'des':des})


# Load all Gatherer Images for Testing
web_imgs_names = []
for (dirpath, dirnames, filenames) in walk('./resources/test_web/'):
    web_imgs_names.extend(filenames)
    break

web_imgs = []

for name in web_imgs_names:
    path = './resources/test_web/' + name
    img = cv2.imread(path,0)
    kp, des = orb.detectAndCompute(img,None)
    web_imgs.append({'name':name,
                     'img':img,
                     'kp':kp,
                     'des':des})

#test_imgs contains camera pics
#web_imgs  contains gatherer pics

#Create Brute Force Matcher Object
bf = cv2.BFMatcher(cv2.NORM_HAMMING)

#Create FLANN Matcher Object TODO


def ratioTest(matcher,des1,des2):
    good_matches = []
    matches = matcher.knnMatch(des1,des2,k=2)
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good_matches.append(m)
    return good_matches

good = 0
bad = 0

for test_card in test_imgs:
    best_num = 0
    best_match = None
    for web_card in web_imgs:
        #matches = bf.match(test_card['des'],web_card['des'])
        matches = ratioTest(bf,test_card['des'],web_card['des'])
        if len(matches) > best_num:
            best_num = len(matches)
            best_match = web_card
    print(test_card['name'],"=>",best_match['name'],"Matches:",best_num)
    if test_card['name'][:3] == best_match['name'][:3]:
        good += 1
    else:
        bad  += 1

print('Accuracy:',str(int((good/(good+bad))*100))+'%')
