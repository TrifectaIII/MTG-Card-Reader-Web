# Main Bottle App File for https://github.com/TrifectaIII/MTG-Card-Reader-Web
# Handles routing of HTTP requests

import os

import bottle

import Identification
import Util


# change working directory to directory of file
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# construct identifier
identifier = Identification.Identifier()


# Serve Main Page
@bottle.route("/")
def index():
    return bottle.static_file("static/index.html", root=".")


# Serve Static Files
@bottle.route("/static/<filepath:path>")
def send_static(filepath):
    return bottle.static_file(filepath, root="./static/")


# Request for Card Match, returns an sfid
@bottle.route("/identify_card", method="POST")
def identify_card():

    # Read Image and Setcode from Request Form
    img_uri = bottle.request.forms.get("image")
    setcode = bottle.request.forms.get("setcode")

    # parse uri into image
    try:
        img_cv2 = Util.uriToCv2(img_uri)
    except Exception as e:
        raise bottle.HTTPError(
            status=400, body="Failed to parse data into valid image."
        )

    # identify card
    cardMatch: Identification.Match | None = identifier.identify(img_cv2)
    if cardMatch == None:
        raise bottle.HTTPError(status=404, body="No card match found.")
    return cardMatch.sfid


# Setup for pythonanywhere
application = bottle.default_app()


# Start localhost Development Server (For Local Machine Use) if this is Main file
if __name__ == "__main__":
    bottle.run(host="localhost", port=8000, debug=True)
