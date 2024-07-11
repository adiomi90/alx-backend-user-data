#!/usr/bin/env python3
""" Module of Users views
"""
import os
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """
    Handle user login

    This function handles the login process for users using session authentication.
    It expects the email and password to be provided in the request form data.
    If the email or password is missing, it returns an error message.
    If the email is not associated with any user, it returns an error message.
    If the password is incorrect, it returns an error message.
    If the login is successful, it creates a session for the user and returns the user's information.

    Returns:
        A dictionary representation of the user if found, else an error message.

    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            resp.set_cookie(session_name, session_id)
            return resp
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout():
    """
    Handle user logout

    This function handles the logout process for users using session authentication.
    It destroys the session associated with the current request.

    Returns:
        An empty JSON response if the session is successfully destroyed, else a 404 error.

    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
