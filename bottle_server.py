from bottle import route, run, debug, template, request, static_file
import os
import time

# Self Defined Matching Package which relies on cv2 and numpy
import matching

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


##################################################################################


# Accept Request for Set Load
@route('/load_set', method='POST')
def load_set():
    print(request.body.read())  # has form of bytestring
    return "load_set not fully implemented yet"

# Accept Request for Card Match
@route('/match_card', method='POST')
def match_card():
    cam_png_uri = request.body.read()  # Read body of post request
    card_name = matching.match(cam_png_uri)
    return card_name


##################################################################################


# Serve Main Page
@route('/')
def index():
    return template('index.html', request=request)

# Serve Static Files
@route('/<filepath:path>')
def send_static(filepath):
    return static_file(filepath, root='.')


##################################################################################


run(host='localhost', port=8000, debug=True)
