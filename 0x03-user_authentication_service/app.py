#!/usr/bin/env python3
"""Module basic flask app"""

from flask import Flask, jsonify, request, abort, Response, redirect
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
def login() -> str:
    """ log in and return session id"""
    email = request.form["email"]
    password = request.form["password"]

    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    msg = {"email": email, "message": "logged in"}
    response = jsonify(msg)
    """response = Flask.make_response(res)"""
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """find the user and destroy the session then redirect
    if exist else respond with 403 HTTP status"""
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """200 HTTP status if the user exist
    otherwise respond with 403 HTTP status"""
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
