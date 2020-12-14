import multiprocessing as mp
import cv2

# Create Brute Force Matcher Object
bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# create multiprocess pool
pool = mp.Pool(mp.cpu_count())


# Counts Number of Good Matches using Ratio Test
def ratioTestCount(sfid, des1, des2):
    good_matches = 0
    global bf
    matches = bf.knnMatch(des1, des2, k=2)
    for pair in matches:
        try:
            m, n = pair
            if m.distance < 0.75*n.distance:
                good_matches += 1
        except ValueError:
            pass
    return (sfid, good_matches)


# returns sfid of best card match
def getMatch(desCam, desDict):

    # # create multiprocess pool
    # pool = mp.Pool(mp.cpu_count())
    global pool

    # collect info for pool map
    RTC_args = []
    for sfid in (list(desDict.keys())):
        des = desDict[sfid]
        RTC_args.append((sfid,desCam,des))
    
    # use multiprocess to calcuate matches of every card
    results = pool.starmap(ratioTestCount, RTC_args)
    # #mark pool for close afterwards
    # pool.close()

    # Find Best Match
    bestCount = 0
    bestSFID = ''
    for (sfid, matchCount) in results:
        if matchCount > bestCount:
            bestCount = matchCount
            bestSFID = sfid

    return bestSFID

