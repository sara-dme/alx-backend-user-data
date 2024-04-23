#!/usr/bin/env python3
"""
Module file
"""
import bcrypt

def _hash_password(password: str) -> bytes:
    """ return a hash password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())