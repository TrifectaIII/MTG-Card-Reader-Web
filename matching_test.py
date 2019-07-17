import cv2
import numpy as np
import pickle

from os import walk

setsGen = []


for (dirpath, dirnames, filenames) in walk("setDes/"):
    for fn in filenames:
        setsGen.append(fn[3:-4])  # cuts off the leading 'set' and trailing '.des'
    break
setsGen.sort()

setsDict = dict()
for setcode in setsGen:
    with open("setDes/set" + setcode + ".des", "rb") as des_file:
        set_names, set_mvids, set_des = pickle.load(des_file)
    setsDict[setcode] = (set_names, set_mvids, set_des)

deslist = []
total = 0
unique = 0


# for key in setsDict:
set_des = setsDict["M10"][2]
for card_des in set_des:
    for des in card_des:
        des = list(des)
        total += 1
        print(total)
        if not (des in deslist):
            unique += 1
            deslist.append(des)

print("Total:", total)
print("Unique:", unique)
