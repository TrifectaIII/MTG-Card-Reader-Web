from __future__ import annotations

import json

ScryfallId = str


class MtgCard:
    def __init__(self, sfid: ScryfallId, name: str) -> None:
        self.sfid = sfid
        self.name = name

    MtgCardDict = dict[ScryfallId, str]

    def toDict(self) -> MtgCardDict:
        return {"sfid": self.sfid, "name": self.name}

    @staticmethod
    def fromMtgJsonCard(mtgJsonCard: dict) -> MtgCard | None:
        # convert from card-set spec here: https://mtgjson.com/data-models/card-set/
        # return None if malformed
        try:
            return MtgCard(
                mtgJsonCard["identifiers"]["scryfallId"], mtgJsonCard["name"]
            )
        except:
            return None


SetCode = str


class MtgSet:
    def __init__(
        self, setCode: SetCode, name: str, mtgCards: dict[ScryfallId, MtgCard]
    ) -> None:
        self.setCode = setCode
        self.name = name
        self.mtgCards = mtgCards

    def getCardBySfid(self, sfid: ScryfallId) -> MtgCard:
        try:
            return self.mtgCards[sfid]
        except KeyError:
            raise KeyError(
                "SFID [{}] could not be found in set [{} {}]".format(
                    sfid, self.setCode, self.name
                )
            )

    def getCards(self) -> set[MtgCard]:
        return set(self.mtgCards.values())

    MtgSetDict = dict[str, str | dict[ScryfallId, MtgCard.MtgCardDict]]

    def toDict(self) -> MtgSetDict:
        return {
            "setCode": self.setCode,
            "name": self.name,
            "mtgCards": {sfid: card.toDict() for (sfid, card) in self.mtgCards.items()},
        }

    @staticmethod
    def fromMtgJsonSet(mtgJsonSet: dict) -> MtgSet | None:
        # convert from set spec here: https://mtgjson.com/data-models/set/
        # return None if malformed, or set has no sfid cards
        try:
            cards: dict[str, MtgCard] = {
                card.sfid: card
                for card in map(MtgCard.fromMtgJsonCard, mtgJsonSet["cards"])
                if card
            }
            if not len(cards.keys()):
                return None
            return MtgSet(mtgJsonSet["code"], mtgJsonSet["name"], cards)
        except:
            return None


class MtgData:
    def __init__(self, sets: dict[SetCode, MtgSet]) -> None:
        self.mtgSets = sets

    def getSetByCode(self, setCode: SetCode) -> MtgSet:
        try:
            return self.mtgSets[setCode]
        except KeyError:
            raise KeyError("SetCode [{}] could not be found".format(setCode))

    def getSets(self) -> set[MtgSet]:
        return set(self.mtgSets.values())

    def getCards(self) -> set[MtgCard]:
        mtgCards: set[MtgCard] = set()
        for mtgSet in self.mtgSets.values():
            mtgCards = mtgCards.union(mtgSet.getCards())
        return mtgCards

    MtgDataDict = dict[SetCode, MtgSet.MtgSetDict]

    def toDict(self) -> MtgDataDict:
        # convert this object to simple dict
        return {setCode: mtgSet.toDict() for (setCode, mtgSet) in self.mtgSets.items()}

    def toJson(self) -> str:
        # convert this object to json string
        return json.dumps(self.toDict())

    @staticmethod
    def fromMtgJson(mtgJson: str) -> MtgData:
        # convert from top level file here: https://mtgjson.com/downloads/all-files/#allprintings

        # read into dict
        # all sets in data space for MTGJSONv5
        mtgJsonData = json.loads(mtgJson)["data"]

        # map function and filter results
        return MtgData(
            {
                set.setCode: set
                for set in map(MtgSet.fromMtgJsonSet, mtgJsonData.values())
                if set
            }
        )


if __name__ == "__main__":
    pass
