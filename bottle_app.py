# Main Bottle App File for https://github.com/TrifectaIII/MTG-Card-Reader-Web
# Handles routing of HTTP requests

from bottle import route, run, request, static_file, default_app
import os

# Self Defined Matching Package which relies on cv2 and numpy
import identification

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Tells Matching.py to Load all files into memory
# Comment out to revert to loading files upon request
identification.loadAllFiles()


##################################################################################


# Accept Request for Card Match
@route("/identify_card", method="POST")
def identify_card():
    # Read Image and Setcode from Request Form
    img_uri = request.forms.get("image")
    setcode = request.forms.get("setcode")
    card_dict = identification.identify(img_uri, setcode)
    return card_dict


##################################################################################


# Serve Main Page
@route("/")
def index():
    return static_file("static/index.html", root=".")


# Serve Static Files
@route("/static/<filepath:path>")
def send_static(filepath):
    return static_file(filepath, root="./static/")


##################################################################################

# Setup for pythonanywhere
application = default_app()

# Start localhost Development Server (For Local Machine Use) If this is Main file
if __name__ == "__main__":
    run(host="localhost", port=8000, debug=True)
