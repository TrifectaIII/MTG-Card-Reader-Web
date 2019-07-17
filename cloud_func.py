import numpy as np
import cv2, json, pickle, base64


def ratioTestCount(request):
    # Counts Number of Good Matches using Ratio Test ()
    request_json = request.get_json()
    if request.args and "message" in request.args:
        obj = request.args.get("message")
    elif request_json and "message" in request_json:
        obj = request_json["message"]
    else:
        return "None"
    star = base64.urlsafe_b64decode(obj.encode())
    des1, des2, mvid = pickle.loads(star)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    good_matches = 0
    matches = matcher.knnMatch(des1, des2, k=2)
    for pair in matches:
        try:
            m, n = pair
            if m.distance < 0.75 * n.distance:
                good_matches += 1
        except ValueError:
            pass
    return json.dumps(good_matches, mvid)


# def ratioTestCount(obj):
#     # Counts Number of Good Matches using Ratio Test ()
#     star = base64.urlsafe_b64decode(obj.encode())
#     des1, des2, mvid = pickle.loads(star)
#     breakpoint()
#     matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
#     good_matches = 0
#     matches = matcher.knnMatch(des1, des2, k=2)
#     for pair in matches:
#         try:
#             m, n = pair
#             if m.distance < 0.75 * n.distance:
#                 good_matches += 1
#         except ValueError:
#             pass
#     return json.dumps(good_matches, mvid)
