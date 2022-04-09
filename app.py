import os, pprint, billboard, random, json
from platform import release
import discogs_client
from flask import Flask
from flask import render_template

discogsToken = "ynOcwonUjpPJlDbHxHwPrGUWBoUwYeTSOqyNkXrt"
app = Flask(__name__)

# Return album cover thing
def pickNew():
    ready = False
    releases = ""
    while not ready:
        try:
            d = discogs_client.Client('SillyAlbumGame/0.1', user_token=discogsToken)
            chart = billboard.ChartData('hot-100')
            song = random.choice(chart)
            releases = d.search(song.title, artist=song.artist, type='release').page(0)[0].images[0]
            ready = True
        except:
            pass
    releases = str(releases)
    releases = releases[releases.index("'uri': '")+8:]
    releases = releases[:releases.index("'")]    
    return(str(releases))

# Serve main site
@app.route('/')
def hello(name=None):
    return render_template('index.html')