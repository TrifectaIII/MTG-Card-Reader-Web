import json
import requests
import os


def changeDirectory() -> None:
    # change working directory to directory of file

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


def cacheResult(func):
    # Function Decorator for Cacheing Results

    cache = dict()

    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@cacheResult
def getMtgJson() -> str:
    # Fetch JSON File from MTGJSON 

    # url for MTGJSONv5 API
    url = 'https://mtgjson.com/api/v5/AllPrintings.json'

    # need user agent header to avoid 403
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

    print("Fetching MTGJSON File from MTGJSON: " + url)

    # send request and recieve response
    response = requests.get(url, headers=headers)

    # make sure response was successful
    if response.status_code == 200:
        return response.content.decode("utf-8")
    else:
        raise Exception("Could not get MTGJSON File, STATUS CODE: " + str(response.status_code))


def downloadMtgJson() -> None:
    # Download JSON File from MTGJSON 

    print("Saving MTGJSON File")

    changeDirectory()

    with open('resources/AllPrintings.json', 'w') as json_file:
        json_file.write(getMtgJson())


def parseMtgJson() -> dict:
    # Parse JSON File from MTGJSON

    # all sets in data space for MTGJSONv5
    return json.loads(getMtgJson())["data"]


def getSetsWithSfids() -> dict[str, str]:
    # return dict of all sets that have sfids
    # setcodes are keys, names are values

    jsonData = parseMtgJson()

    setsWithSfids: dict[str, str] = dict()

    # loop through each set
    for setCode in (list(jsonData.keys())):
        # loop through each card in the set
        for card in jsonData[setCode]['cards']:
            if "identifiers" in card and "scryfallId" in card["identifiers"]:
                # add to dict if at least 1 card has a scryfall id
                setsWithSfids[setCode] = jsonData[setCode]['name']
                break
    
    return setsWithSfids


def saveSetsWithSfids() -> None:
    # Save sets dict as json file

    print("Saving Sets Info")

    changeDirectory()

    with open('static/sets.json','w') as jsonfile:
        json.dump(getSetsWithSfids(), jsonfile)


def getSfids() -> dict[str, str]:
    # Save dictionary of all sfids as keys and names as values

    jsonData = parseMtgJson()

    sfidDict = dict()

    for set in (list(jsonData.keys())):
        cards = jsonData[set]['cards']
        for card in cards:
            try:
                sfid = card['identifiers']['scryfallId']
                name = card['name']
            except:
                pass
            else:
                sfidDict[sfid] = name

    return sfidDict


def saveSfids() -> None:
    # save sfid dict as json file

    print("Saving Sets Info")

    changeDirectory()

    with open('resources/cardsInfo.json','w') as jsonfile:
        json.dump(getSfids(), jsonfile)
