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

# img = test_imgs[0]['img']
# kp = test_imgs[0]['kp']
# img2 = cv2.drawKeypoints(img,kp,None,color=(0,255,0), flags=0)
# plt.imshow(img2),plt.show()

