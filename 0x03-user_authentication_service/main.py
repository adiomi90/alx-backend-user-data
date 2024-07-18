#!/usr/bin/env python3
"""
Main file for the API module for the user authentication service.
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Register a new user.

    Args:
        email (str): The email address of the user.
        password (str): The password for the user.

    Returns:
        None

    Raises:
        AssertionError: If the registration fails or the response
        status code is not 200 or 400.
    """
    resp = requests.post('http://127.0.0.1:5000/users',
                         data={'email': email, 'password': password})
    if resp.status_code == 200:
        assert (resp.json() == {"email": email, "message": "user created"})
    else:
        assert (resp.status_code == 400)
        assert (resp.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Attempt to log in with the wrong password.

    Args:
        email (str): The email address of the user.
        password (str): The wrong password.

    Returns:
        None

    Raises:
        AssertionError: If the login attempt succeeds or the response
        status code is not 401.
    """
    r = requests.post('http://127.0.0.1:5000/sessions',
                      data={'email': email, 'password': password})
    assert (r.status_code == 401)


def profile_unlogged() -> None:
    """
    Access the profile page without logging in.

    Returns:
        None

    Raises:
        AssertionError: If the access to the profile page succeeds
        or the response status code is not 403.
    """
    r = requests.get('http://127.0.0.1:5000/profile')
    assert (r.status_code == 403)


def log_in(email: str, password: str) -> str:
    """
    Log in a user.

    Args:
        email (str): The email address of the user.
        password (str): The password for the user.

    Returns:
        str: The session ID.

    Raises:
        AssertionError: If the login fails or the
        response status code is not 200.
    """
    resp = requests.post('http://127.0.0.1:5000/sessions',
                         data={'email': email, 'password': password})
    assert (resp.status_code == 200)
    assert (resp.json() == {"email": email, "message": "logged in"})
    return resp.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """
    Access the profile page after logging in.

    Args:
        session_id (str): The session ID.

    Returns:
        None

    Raises:
        AssertionError: If the access to the profile page
        fails or the response status code is not 200.
    """
    cookies = {'session_id': session_id}
    r = requests.get('http://127.0.0.1:5000/profile',
                     cookies=cookies)
    assert (r.status_code == 200)


def log_out(session_id: str) -> None:
    """
    Log out a user.

    Args:
        session_id (str): The session ID.

    Returns:
        None

    Raises:
        AssertionError: If the logout fails or the response
        status code is not 200 or 302.
    """
    cookies = {'session_id': session_id}
    r = requests.delete('http://127.0.0.1:5000/sessions',
                        cookies=cookies)
    if r.status_code == 302:
        assert (r.url == 'http://127.0.0.1:5000/')
    else:
        assert (r.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    Get the reset token for password reset.

    Args:
        email (str): The email address of the user.

    Returns:
        str: The reset token.

    Raises:
        AssertionError: If the request for reset token fails
        or the response status code is not 200 or 401.
    """
    r = requests.post('http://127.0.0.1:5000/reset_password',
                      data={'email': email})
    if r.status_code == 200:
        return r.json()['reset_token']
    assert (r.status_code == 401)


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """
    Update the password for a user.

    Args:
        email (str): The email address of the user.
        reset_token (str): The reset token for password reset.
        new_password (str): The new password to be set.

    Returns:
        None

    Raises:
        AssertionError: If the password update fails
        or the response status code is not 200 or 403.
    """
    data = {'email': email, 'reset_token': reset_token,
            'new_password': new_password}
    r = requests.put('http://127.0.0.1:5000/reset_password',
                     data=data)
    if r.status_code == 200:
        assert (r.json() == {"email": email, "message": "Password updated"})
    else:
        assert (r.status_code == 403)


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
