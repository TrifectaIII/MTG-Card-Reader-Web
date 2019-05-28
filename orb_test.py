import numpy as np 
import cv2
from os import walk

# Test the Matching Ability of ORB (Oriented FAST Rotated BRIEF)


# Load all Cam Images for Testing
test_imgs_names = []
for (dirpath, dirnames, filenames) in walk('./resources/test_cam/'):
    test_imgs_names.extend(filenames)
    break

test_imgs = []

for name in test_imgs_names:
    path = './resources/test_cam/' + name
    img = cv2.imread(path,0)
    test_imgs.append({'name':name,'img':img})


# Load all Gatherer Images for Testing
web_imgs_names = []
for (dirpath, dirnames, filenames) in walk('./resources/test_web/'):
    web_imgs_names.extend(filenames)
    break

web_imgs = []

for name in web_imgs_names:
    path = './resources/test_web/' + name
    img = cv2.imread(path,0)
    web_imgs.append({'name':name,'img':img})

#test_imgs contains camera pics
#web_imgs  contains gatherer pics
