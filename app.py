
# Libraries to import
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Flask initialization settings
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# The structure of the data from records.db
class Album(db.Model):
    __tablename__ = "album"
    file = db.Column(db.String, primary_key=True)
    artist = db.Column(db.String)
    album = db.Column(db.String)

# Serve main site
@app.route('/')
def main():
    return render_template(

        # The HTML file for the results
        'index.html',

        # Sets the 'file' variable to a random filename
        file=Album.query.order_by(func.random()).first().file)