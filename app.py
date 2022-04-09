import os, pprint, billboard, random, json
from platform import release
import discogs_client
import flask

discogsToken = "ynOcwonUjpPJlDbHxHwPrGUWBoUwYeTSOqyNkXrt"

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

print(pickNew())