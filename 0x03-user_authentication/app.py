#!/usr/bin/env python3
"""
Flask app for user authentication.

This app provides endpoints for user registration,
login, logout, profile retrieval,
password reset token generation, and password update.

Endpoints:
- GET /: Returns a JSON response with a welcome message.
- POST /users: Registers a new user with the provided emailand password.
- POST /sessions: Logs in a user with the provided email and password.
- DELETE /sessions: Logs out the currently logged-in user.
- GET /profile: Retrieves the profile of the currently logged-in user.
- POST /reset_password: Generates a reset password token for the
provided email.
- PUT /reset_password: Updates the password for the provided email
using the reset token.

"""

from flask import (
    Flask,
    request,
    jsonify,
    abort,
    redirect,
    url_for
)

from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Return json respomse
    {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:

    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    Logs in a user by validating the provided email and password.

    Returns:
        str: A JSON response containing the user's email and a success message.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    resp = jsonify({"email": f"{email}", "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Logs out the user by destroying the session and redirecting
    to the homepage.

    Returns:
        A redirect response to the homepage.

    Raises:
        HTTPException: If the user is not authenticated or the
        session ID is missing.
    """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None or session_id is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    Retrieves the user's profile information.

    Returns:
        A JSON response containing the user's email if the user
        is authenticated. Otherwise, returns a 403 Forbidden error.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Retrieves the reset password token for a given email address.

    Returns:
        str: The reset password token.

    Raises:
        HTTPException: If the email address is not valid.
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """
    Update the password for a user.

    Retrieves the email, reset token, and new password from the request form.
    Calls the `update_password` method of the `AUTH` object to update the
    password. If the reset token is invalid, raises a `ValueError` and returns
    a 403 error response.
    Returns a JSON response with the updated email and a success message.

    Returns:
        str: JSON response with the updated email and a success message.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": f"{email}", "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
