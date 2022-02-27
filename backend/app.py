### IMPORTS #########
from flask import Flask, send_from_directory, abort, request    # The Main Flask App thing, and send_from_directory to serve static files from local directory
import requests                                 # for API requests
import json                                     # To parse and send JSON objects to and from the svelte front-end
from datetime import datetime                   # getting current local time and checking for nighttime

import weather_report                 # my script to fetch weather conditions and generate the weather cards
from flask import send_file

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

# BACKEND :: Fetch current weather conditions and weather forecast for the day
@app.route('/wttr/<city>')
def wttr(city: str):
    # Get the weather card as a PNG BytesIO object
    try:
        weather_card = weather_report.weather_report(city)
        weather_card.seek(0)
        return send_file(weather_card, mimetype='image/png')# as_attachment=True, attachment_filename='weather_card.png')

    # Returning a 404 Error if the given city resulted in error
    except ValueError:
        abort(404)

# BACKEND :: Fetch tomorrow's weather forecast and average condition
@app.route('/tmrw/<city>')
def tomorrow(city: str):
    transparent = request.args.get('transparent', default=False, type=lambda v: v.lower() == 'true')   # whether the card should be solid white or transparent (aka light vs dark mode)

    # Get the weather card as a PNG BytesIO object
    try:
        weather_card = weather_report.tomorrow(city, transparent)
        weather_card.seek(0)
        return send_file(weather_card, mimetype='image/png')

    # Returning a 404 Error if the given city resulted in error
    except ValueError:
        return send_file(weather_card, mimetype='image/png')


### RUNNING THE WEBSITE #########
if __name__ == '__main__':   
    app.run(debug=True)