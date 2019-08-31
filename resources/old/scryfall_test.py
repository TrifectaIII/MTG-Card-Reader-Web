import cv2
from urllib import request as urlreq
import numpy as np

def getCvImageByMVID(mvid):
    response = urlreq.urlopen('https://api.scryfall.com/cards/multiverse/{}/?format=image&version=border_crop'.format(str(mvid)))
    nparr = np.frombuffer(response.read(), np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np

# api request formatting: only needs mvid as show 
# https://api.scryfall.com/cards/<MVID HERE>/409574/?format=image&version=border_crop

# img_np = getCvImageByMVID(442130)
# cv2.imshow('img_np',img_np)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
