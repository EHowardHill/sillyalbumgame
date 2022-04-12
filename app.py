
# Libraries to import
import julian, datetime
from os import path, listdir, getcwd
from flask import Flask, render_template, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from PIL import Image
from math import floor

# Flask initialization settings
app = Flask(__name__)

# You have to choose an arbitrary secret key in order to
# encrypt the stored result. It can be literally anything
app.secret_key = "silly billy willy"
app.config['SESSION_TYPE'] = 'refis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# The structure of the data from records.db
class Album(db.Model):
    __tablename__ = "album"
    file = db.Column(db.String, primary_key=True)
    artist = db.Column(db.String)
    album = db.Column(db.String)

class Daily(db.Model):
    __tablename__ = "daily"
    day = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String)

# Serve main site
@app.route('/')
def main():

    jd = floor(julian.to_jd(datetime.datetime.now()))
    history = Daily.query.filter(Daily.day == jd).all()
    my_choice = None

    # Choose new image
    if len(history) == 0:
        my_choice = Album.query.order_by(func.random()).first()
        d = Daily(day=jd, file=my_choice.file)
        db.session.add(d)
        db.session.commit()
        session['score'] = 0

    # Use existing image
    else:
        my_choice = Album.query.filter(Album.file==history[0].file).first()

    score = 0
    success = False

    # If you're good for the day
    if len(session.keys()) > 0:
        score = session['score'] 
        success = session['success']

    return render_template(

        # The HTML file for the results
        'index.html',

        # Sets the 'file' variable to a random filename
        file=my_choice.file,
        album=my_choice.album,
        artist=my_choice.artist,
        albums=','.join(["\"" + str(x.album) + " (" + str(x.artist) + ")\"" for x in Album.query.all()]),
        score=score,
        success=success
    )

# Handle session
@app.route('/score', methods=['POST'])
def score():
    print("recording...")
    session['score'] = request.form["score"]
    session['success'] = request.form["success"]
    return score

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)