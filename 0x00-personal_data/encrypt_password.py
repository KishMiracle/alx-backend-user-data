#!/usr/bin/env python3
import bcrypt


def hash_password(password):
    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password
