#!/usr/bin/env python3
import bcrypt


def is_valid(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
