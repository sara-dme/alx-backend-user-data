#!/usr/bin/env python3
"""Module basic flask app"""

from flask import Flask, jsonify, make_response, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

@app.route("/sessions", methods=['POST'])
def login() -> str:
    """ log in and return session id"""
    try:
        email = request.form.get['email']
        password  = request.form.get['password']
    except KeyError:
        abort(400)
    if AUTH.valid_login(email, password):
        response = make_response(jsonify({"email": email, "message": "logged in"}), 200)
        response.set_cookie("session_id", AUTH.create_session(email))
        return response
    abort(401)

@app.route('/', methods=["GET"])
def hello_world():
    """ for authentication service API"""
    msg = {"message": "Bienvenu"}
    return jsonify(msg)


@app.route("/users", methods=["POST"])
def users():
    """ register a new user if it does not exist"""
    email = request.form["email"]
    password = request.form["password"]
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
