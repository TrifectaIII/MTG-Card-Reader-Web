# Matching Package for https://github.com/TrifectaIII/MTG-Card-Reader-Web
# Handles the matching of webcam images to individual cards
# Uses opencv's ORB feature descriptor

from __future__ import annotations

import concurrent.futures
import itertools
import logging
import pickle
from collections.abc import Iterable

import cv2
import numpy

import Model


class Match:
    def __init__(self, sfid: Model.ScryfallId, count: int) -> None:
        self.sfid = sfid
        self.count = count

    @staticmethod
    def findBest(matches: Iterable[Match | None]) -> Match | None:
        # find the best match from a list

        bestMatch = None

        for match in matches:
            if match == None:
                continue
            if bestMatch == None or match.count > bestMatch.count:
                bestMatch = match

        return bestMatch


class Identifier:
    def __init__(self) -> None:
        # create required cv2 orb and brute force matcher objects
        self.orb = cv2.ORB_create()

        # load descriptor data
        self.descriptors: dict[
            Model.ScryfallId, numpy.ndarray
        ] = Identifier.loadCards()

        # create process pool
        self.processExecutor = concurrent.futures.ProcessPoolExecutor()

        logging.info("Identifier Booted Up")

    @staticmethod
    def compare(
        sfid: Model.ScryfallId, des1: numpy.ndarray, des2: numpy.ndarray
    ) -> Match | None:
        # Counts Number of Good Descriptor Matches using Ratio Test
        
        good_matches = 0
        for pair in cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(des1, des2, k=2):
            try:
                m, n = pair
                if m.distance < 0.75 * n.distance:
                    good_matches += 1
            except ValueError:
                pass
        if good_matches == 0:
            return None
        return Match(sfid, good_matches)

    def identify(self, img) -> Match | None:
        # Matches image to a card

        # Detect and Compute ORB Descriptors
        _, des = self.orb.detectAndCompute(img, None)
        imageDescription: numpy.ndarray = des

        # create iterators for mapping
        sfids: list[Model.ScryfallId] = []
        imageDescriptions: Iterable[numpy.ndarray] = itertools.cycle([imageDescription])
        cardDescriptions: list[numpy.ndarray] = []
        for sfid, cardDescription in self.descriptors.items():
            sfids.append(sfid)
            cardDescriptions.append(cardDescription)

        # send to process pool
        futures = self.processExecutor.map(
            Identifier.compare, sfids, imageDescriptions, cardDescriptions
        )

        # find the best of the bunch
        return Match.findBest(futures)

    def identifyNoPool(self, img) -> Match | None:
        # Matches image to a card without using process pool

        # Detect and Compute ORB Descriptors
        _, des = self.orb.detectAndCompute(img, None)
        imageDescription: numpy.ndarray = des

        # create iterators for mapping
        sfids: list[Model.ScryfallId] = []
        imageDescriptions: Iterable[numpy.ndarray] = itertools.cycle([imageDescription])
        cardDescriptions: list[numpy.ndarray] = []
        for sfid, cardDescription in self.descriptors.items():
            sfids.append(sfid)
            cardDescriptions.append(cardDescription)

        # map without processes
        futures = map(
            Identifier.compare, sfids, imageDescriptions, cardDescriptions
        )

        # find the best of the bunch
        return Match.findBest(futures)


    @staticmethod
    def loadCards() -> dict[Model.ScryfallId, numpy.ndarray]:
        # Load All SetDes files to Memory

        from os import walk

        setsGen = []
        for (_, _, filenames) in walk("setDes"):
            for fn in filenames:
                setsGen.append(
                    fn[3:-4]
                )  # cuts off the leading 'set' and trailing '.des'
            break
        setsGen.sort()

        combinedDict: dict[Model.ScryfallId, numpy.ndarray] = {}

        for setcode in setsGen:
            with open("setDes/set" + setcode + ".pkl", "rb") as des_file:
                combinedDict.update(pickle.load(des_file))

        logging.info("Loaded Card Descriptor Data")
        return combinedDict

    def reloadCards(self) -> None:
        # reload from source
        self.descriptors = Identifier.loadCards()


if __name__ == "__main__":
    pass
