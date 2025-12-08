### IMPORTS #########
from flask import Flask, send_from_directory, abort, request    # The Main Flask App thing, and send_from_directory to serve static files from local directory

import weather_report
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
    try:
        weather_card = weather_report.weather_report(city)
        weather_card.seek(0)
        return send_file(weather_card, mimetype='image/png')# as_attachment=True, attachment_filename='weather_card.png')

    except ValueError:
        abort(404, "city not found :(")

# BACKEND :: Fetch tomorrow's weather forecast and average condition
@app.route('/tmrw/<city>')
def tomorrow(city: str):
    transparent = request.args.get('transparent', default=False, type=lambda v: v.lower() == 'true')   # whether the card should be solid white or transparent (aka light vs dark mode)

    try:
        weather_card = weather_report.tomorrow(city, transparent)
        weather_card.seek(0)
        return send_file(weather_card, mimetype='image/png')

    except ValueError:
        abort(404, "city not found :(")

@app.route('/api/<city>')
def api(city: str):
    try:
        return weather_report.get_weather_report_data(city).model_dump()
    
    except ValueError:
        abort(500, "yikes")

### RUNNING THE WEBSITE #########
if __name__ == '__main__':   
    app.run(debug=True)