from multiprocessing import Pool, cpu_count
import cv2
import pickle, base64
import requests

# FLANN_INDEX_LSH = 6
# index_params= dict(algorithm = FLANN_INDEX_LSH,
#                    table_number = 4, # 12
#                    key_size = 10,     # 20
#                    multi_probe_level = 2) #2
# search_params = dict(checks=100)   # or pass empty dictionary

# matcher = cv2.FlannBasedMatcher(index_params,search_params)
matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
curl = "https://us-central1-api-project-479074902481.cloudfunctions.net/function-1"
cv2.ocl.setUseOpenCL(not True)


def ratioTestCount(des1, desDict):
    # Counts Number of Good Matches using Ratio Test ()
    best_match_count = 0
    best_mvid = None
    for mvid, des2 in desDict.items():
        good_matches = 0
        matches = matcher.knnMatch(des1, des2, k=2)
        for pair in matches:
            try:
                m, n = pair
                if m.distance < 0.75 * n.distance:
                    good_matches += 1
            except ValueError:
                pass
        if good_matches > best_match_count:
            best_match_count = good_matches
            best_mvid = mvid
    return best_match_count, best_mvid


def cloud_func(x, y, z):
    return requests.post(
        curl,
        json={"message": base64.urlsafe_b64encode(pickle.dumps([x, y, z])).decode()},
    )


pool = Pool(cpu_count())
