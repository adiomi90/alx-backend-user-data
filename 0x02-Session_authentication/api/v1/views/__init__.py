#!/usr/bin/env python3
from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
"""This module initializes the views blueprint for the API.

It imports the necessary modules and sets up the blueprint with a URL prefix.
"""
User.load_from_file()
