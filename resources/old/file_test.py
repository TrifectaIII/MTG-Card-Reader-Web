import numpy as np
import cv2
from os import walk
import pickle

# Test the Ability to Save Descriptors to File

# Setup ORB and Matcher

orb = cv2.ORB_create()

bf = cv2.BFMatcher(cv2.NORM_HAMMING)


def ratioTestCount(matcher, des1, des2):
    # Counts Number of Good Matches using Ratio Test ()
    good_matches = []
    matches = matcher.knnMatch(des1, des2, k=2)
    for pair in matches:
        try:
            m, n = pair
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        except ValueError:
            pass
    return len(good_matches)


# Load all Cam Images for Testing
test_imgs_names = []
for (dirpath, dirnames, filenames) in walk("./resources/test_cam/"):
    test_imgs_names.extend(filenames)
    break

test_imgs = []

for name in test_imgs_names:
    path = "./resources/test_cam/" + name
    img = cv2.imread(path, 0)
    kp, des = orb.detectAndCompute(img, None)
    test_imgs.append({"name": name, "img": img, "kp": kp, "des": des})


# Load all Gatherer Images for Testing
web_imgs_names = []
for (dirpath, dirnames, filenames) in walk("./resources/test_web/"):
    web_imgs_names.extend(filenames)
    break

web_imgs = []

for name in web_imgs_names:
    path = "./resources/test_web/" + name
    img = cv2.imread(path, 0)
    kp, des = orb.detectAndCompute(img, None)
    web_imgs.append({"name": name, "img": img, "kp": kp, "des": des})

# test_imgs contains camera pics
# web_imgs  contains gatherer pics


# Generate File with Dictionary of Web
set_dict = dict()

for card in web_imgs:
    set_dict[card["name"]] = card["des"]

filename = "set.des"
outfile = open(filename, "wb")
pickle.dump(set_dict, outfile)
outfile.close()

infile = open(filename, "rb")
file_dict = pickle.load(infile)
infile.close()

# print(file_dict)

name1 = test_imgs[3]["name"]
des1 = test_imgs[3]["des"]

bigCount = 0
bigName = ""

for name in file_dict:
    des = file_dict[name]
    matchCount = ratioTestCount(bf, des1, des)
    if matchCount > bigCount:
        bigCount = matchCount
        bigName = name

print(name1, bigName)
