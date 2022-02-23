### IMPORTS #########
from flask import Flask, send_from_directory    # The Main Flask App thing, and send_from_directory to serve static files from local directory
import requests                                 # for API requests
import json                                     # To parse and send JSON objects to and from the svelte front-end
from datetime import datetime                   # getting current local time and checking for nighttime


### INITIALISING APP #########
app = Flask(__name__)

### ROUTES #########
# SVELTE :: Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('../frontend/public', 'index.html')

# SVELTE :: Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('../frontend/public', path)


### RUNNING THE WEBSITE #########
if __name__ == '__main__':   
    app.run(debug=True)