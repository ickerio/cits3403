from flask import (
    Flask, render_template,
)

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/find-sketch')
def findSketch():
    return render_template('find-sketch.html')

@app.route('/guess-sketch')
def guessSketch():
    return render_template('guess-sketch.html')

@app.route('/draw-sketch')
def drawSketch():
    return render_template('draw-sketch.html')