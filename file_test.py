import numpy as np 
import cv2
from os import walk
import time

#Test the Ability to Save Descriptors to File

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

img = test_imgs['img']
kp  = test_imgs['kp']
des = test_imgs['des']