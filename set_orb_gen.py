import requests
import cairosvg
from tqdm import tqdm
import cv2
import numpy as np
from io import BytesIO, StringIO
from PIL import Image
import os
import pickle

scryfall = "https://api.scryfall.com/sets"

setlist = requests.get(scryfall).json()

orb = cv2.ORB_create()

# s = setlist['data'][200]
# b = StringIO()

# cairosvg.svg2png(url=s['icon_svg_uri'], write_to=b)
# b.seek(0)
# pimg = Image.open(b)
# img = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
# cv2.imwrite('o.jpg', img)

desList = []

# for s in tqdm(setlist['data']):
# 	with BytesIO() as b:
# 		cairosvg.svg2png(url=s['icon_svg_uri'], write_to=b)
# 		b.seek(0)
# 		arr = np.asarray(bytearray(b.read()), dtype=np.uint8)
# 		img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
# 		_, des = orb.detectAndCompute(img, None)
# 		desList.append((s['code'], des))


directory = os.fsencode("set_jpgs")
for filename in os.listdir(directory):
    if filename.endswith(b".jpg"):
        fn = os.path.join(directory, filename).decode("utf-8")
        img = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)
        _, des = orb.detectAndCompute(img, None)
        desList.append((filename.decode("utf-8").split(".")[0], des))
        continue
    else:
        continue


with open("all-sets-orb.pkl", "wb") as f:
    pickle.dump([x for x in desList if x[1] != None], f)
