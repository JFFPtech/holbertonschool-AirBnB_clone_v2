#!/usr/bin/python3
""" Module to start a Flask web application """

from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def hello():
    return 'Hello HBNB!'

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'

@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    return 'C %s' % text.replace('_', ' ')

@app.route('/python/<text>', strict_slashes=False)
def python_route(text='is cool'):
    return 'Python %s' % text.replace('_', ' ')

@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    return '%d is a number' % n

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
