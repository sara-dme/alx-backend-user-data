#!/usr/bin/env python3
"""Module basic flask app"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=["GET"])
def hello_world():
    """ for authentication service API"""
    msg = {"message": "Bienvenu"}
    return jsonify(msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
