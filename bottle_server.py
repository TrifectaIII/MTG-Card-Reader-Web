from bottle import route, run, debug, template, request, static_file
import os
import time
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
counter = 0

@route('/hello')
def hello():
    return "Hello World!"

@route('/')
def index():
    return template('index.html', request=request)

@route('/<filepath:path>')
def send_static(filepath):
    return static_file(filepath,root='.')

@route('/test')
def test():
    global counter
    counter += 1
    return "testing testing " + str(counter)

run(host='localhost', port=8000, debug=True)