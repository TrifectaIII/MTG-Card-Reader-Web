import numpy as np
import cv2
from os import walk
import time

# Test the Matching Ability of ORB (Oriented FAST Rotated BRIEF)

# Setup ORB

orb = cv2.ORB_create()

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

# Create Brute Force Matcher Object
bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# Create FLANN Matcher Object
index_params = dict(
    algorithm=6,  # Algorithm 6 is FLANN_INDEX_LSH
    table_number=6,  # 12
    key_size=12,  # 20
    multi_probe_level=1,
)  # 2
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

# Counts number of good matches based on Lowe Ratio Test
def ratioTestCount(matcher, des1, des2):
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


good = 0
bad = 0

start = time.time()

for test_card in test_imgs:
    best_count = 0
    best_match = None
    for web_card in web_imgs:
        matchCount = ratioTestCount(bf, test_card["des"], web_card["des"])
        if matchCount > best_count:
            best_count = matchCount
            best_match = web_card
    print(
        test_card["name"][:-4], "=>", best_match["name"][:-4], "   Matches:", best_count
    )
    if test_card["name"][:3] == best_match["name"][:3]:
        good += 1
    else:
        bad += 1

print("Accuracy:", str(int((good / (good + bad)) * 100)) + "%")
print("Runtime (sec):", time.time() - start)
