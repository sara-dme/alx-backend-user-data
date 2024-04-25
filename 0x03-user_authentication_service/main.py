#!/usr/bin/env python3
""" End-to-end integration test"""

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """ user registration"""
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/users', data=data)
    msg = {"email": email, "message": "user created"}
    assert response.status_code == 200
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str):
    """ log in with wrong password"""
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/sessions', data=data)
    assert response.status_code == 401


def profile_unlogged():
    """ test for validation profil mlogin without login"""
    cookies = {"session_id": ""}
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """Test for validating succesful log in"""
    data = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/sessions', data=data)
    msg = {"email": email, "message": "user created"}
    assert response.status_code == 200
    assert response.json() == msg
    session_id = response.cookies.get("session_id")
    return session_id


def profile_logged(session_id: str) -> None:
    """Test for validating profile request logged in """
    cookies = {"session_id": ""}
    response = requests.get(f'{BASE_URL}/profile', cookies=cookies)
    msg = {"email": EMAIL}
    assert response.status_code == 200
    assert response.json() == msg


def log_out(session_id: str) -> None:
    """test for valid logout"""
    cookies = {"session_id": ""}
    response = requests.get(f'{BASE_URL}/sessions', cookies=cookies)
    msg = {"message": "Bienvenue"}
    assert response.status_code == 200
    assert response.json() == msg


def reset_password_token(email: str) -> str:
    """test for valid password reset token"""
    data = {"email": email}
    response = requests.post(f'{BASE_URL}/reset_password', data=data)
    reset_token = response.json().get("reset_token")
    msg = {"email": email, "reset_token": reset_token}
    assert response.status_code == 200
    assert response.json() == msg
    return reset_token


def update_password(email: str, reset_token: str, password: str) -> None:
    """ test for valid password reset"""
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": password
    }
    response = requests.put(f'{BASE_URL}/reset_password', data=data)
    msg = {"email": email, "message": "Password updated"}
    assert response.status_code == 200
    assert response.json() == msg


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
