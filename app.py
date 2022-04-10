import os, pprint, billboard, random, json
from platform import release
import discogs_client
from flask import Flask
from flask import render_template

discogsToken = "ynOcwonUjpPJlDbHxHwPrGUWBoUwYeTSOqyNkXrt"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Album(db.Model):
    __tablename__ = "album"
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String)
    artist = db.Column(db.String)
    album = db.Column(db.String)

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
def main():
    return render_template('index.html')