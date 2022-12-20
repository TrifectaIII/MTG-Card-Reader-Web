import logging
import os
import pickle
import time

import cv2
import numpy
import requests

import Model
import MtgJsonUtil


def getDescriptionBySFID(sfid: Model.ScryfallId, orb) -> numpy.ndarray:
    # Function for getting image descriptors with sfid using scryfall api and cv2

    # scryfall api request formatting: only needs sfid
    url = "https://api.scryfall.com/cards/{}/?format=image&version=border_crop".format(
        str(sfid)
    )

    # make request
    try:
        r = requests.get(url, timeout=20)
    except:
        r = None

    # tracks the backoff
    backoffLevel: int = 0

    # continue to retry with exponential backoff, if failed
    while r == None or r.status_code != 200:
        backoffLevel += 1
        backoffSeconds = backoffLevel**backoffLevel
        print(
            "Will retry after " + str(backoffSeconds) + " seconds... SFID: " + str(sfid)
        )
        time.sleep(backoffSeconds)
        try:
            r = requests.get(url, timeout=20)
        except:
            r = None

    # process image when request successful
    np_array = numpy.frombuffer(r.content, numpy.uint8)
    img_np = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
    _, description = orb.detectAndCompute(img_np, None)
    return description


def saveDescriptionsToFiles() -> None:
    # Save each sets descriptors dict as file in setDes

    # setup ORB
    orb = cv2.ORB_create()

    # get data from mtgjson
    mtgData = MtgJsonUtil.parseMtgJson()

    # list of sets, sorted by setcode
    setList = list(mtgData.getSets())
    setList.sort(key=(lambda set: set.setCode))

    # loop through each set
    for mtgSet in setList:

        # SKIP IF FILE EXISTS
        if os.path.isfile("setDes/set" + mtgSet.setCode + ".pkl"):
            print(mtgSet.setCode, "file found, skipping")
            continue

        # init dict
        cardDescriptions: dict[Model.ScryfallId, numpy.ndarray] = {}

        # For each card, save to dictionary
        for mtgCard in mtgSet.getCards():
            print(mtgSet.setCode, mtgCard.name, mtgCard.sfid)

            # time delay to avoid overloading scryfall api
            time.sleep(1)

            # make call and add data
            cardDescriptions[mtgCard.sfid] = getDescriptionBySFID(mtgCard.sfid, orb)

        # save dict to file
        with open("setDes/set" + mtgSet.setCode + ".pkl", "wb") as desciptionFile:
            pickle.dump(cardDescriptions, desciptionFile)


if __name__ == "__main__":
    # change working directory to directory of file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # generate the files
    saveDescriptionsToFiles()
