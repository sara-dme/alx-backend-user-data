#!/usr/bin/env python3
"""Module basic flask app"""

from flask import Flask, jsonify, request, abort, Response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"])
def hello_world() -> Response:
    """ for authentication service API"""
    msg = {"message": "Bienvenu"}
    return jsonify(msg)


@app.route("/users", methods=["POST"])
def users() -> Response:
    """ register a new user if it does not exist"""
    email = request.form["email"]
    password = request.form["password"]
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> Response:
    """ log in and return session id"""
    email = request.form["email"]
    password = request.form["password"]

    if AUTH.valid_login(email, password):
        res = jsonify({"email": email, "message": "logged in"}), 200
        response = Flask.make_response(res)
        response.set_cookie("session_id", AUTH.create_session(email))
        return response
    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
