import base64

import cv2
import numpy


def uriToCv2(img_uri):
    # Converts image from base 64 encoded uri string to cv2 Image

    # Remove URI header from png data
    img_arr = img_uri.split(",")
    img_data = img_arr[1]
    # Decode base64 png/jpg data
    img_data_decode = base64.b64decode(img_data)
    # Create numpy array with png/jpg data
    np_arr = numpy.asarray(bytearray(img_data_decode), dtype=numpy.uint8)
    # Convert numpy array to cv2 image, then return
    img_cv2 = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    return img_cv2


if __name__ == "__main__":
    pass
