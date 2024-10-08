from datetime import timedelta
from flask import Flask, render_template, send_from_directory
from flask_caching import Cache
from modules.simulator import RaceSimulator, Track, Driver
from modules.data import tracks, drivers
import random
import os
# test23441412412412123131313131321312312312312313123132
#oewıfjwjefoqjwfıjwqpef
app = Flask(__name__)

race_simulator = RaceSimulator(tracks, drivers)

app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

@app.template_filter('format_lap_time')
def format_lap_time(value):
    formatted_time = str(timedelta(seconds=value))
    if formatted_time.startswith("0:"):
        formatted_time = formatted_time[2:]
    return formatted_time

@app.route('/')
@cache.cached(timeout=3600)
def index():
    selected_track = random.choice(tracks)
    race_results = race_simulator.simulate_race(selected_track, selected_track.laps)

    return render_template('index.html', track=selected_track, race_results=race_results)

if __name__ == '__main__':
    app.run(debug=True)
