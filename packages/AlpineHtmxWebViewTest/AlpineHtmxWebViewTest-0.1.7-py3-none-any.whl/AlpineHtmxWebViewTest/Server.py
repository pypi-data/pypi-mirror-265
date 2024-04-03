# ----------------------------------------------------------------------
# |
# |  Server.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2024-03-17 16:58:35
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2024
# |  Distributed under the MIT License.
# |
# ----------------------------------------------------------------------
"""Serves content"""

import json

from functools import wraps

import bleach
import webview

from flask import Flask, make_response, render_template, request

app = Flask(__name__)

# pylint: disable=invalid-name


# ----------------------------------------------------------------------
def verify_token(function):
    @wraps(function)
    def Wrapper(*args, **kwargs):
        token = request.args.get("token", None)
        if token is None:
            token = json.loads(request.data).get("token", None)

        if token == webview.token:
            return function(*args, **kwargs)

        raise Exception("Authentication error")

    return Wrapper


# ----------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", token=webview.token)


# ----------------------------------------------------------------------
@app.route("/on_change", methods=["GET", "POST"])
@verify_token
def on_change():
    name = bleach.clean(request.args["name"])

    if not name:
        response = ""
    else:
        if name.lower() == "dave":
            name = f"<span style='color:red;'>{name}</span>"

        response = f"<p>Hello, {name}, from HTMX/Flask!</p>"

    return make_response(response)
