#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Constants for the Salient SDK.

This module contains constants used throughout the Salient SDK.

"""

import datetime
import hashlib
import urllib

import requests

# This is the base URL for the Salient API:
URL = "https://api.salientpredictions.com/"

API_VERSION = "v2"

MODEL_VERSION = "v8"
MODEL_VERSIONS = ["v7", "v7_1", "v8"]

VERFY_SSL = True

TEST_USER = "help+test@salientpredictions.com"
TEST_PWD = "salty!"

CURRENT_SESSION = None


def _build_url(endpoint: str, args: None | dict = None) -> tuple[str, str]:
    url = URL + API_VERSION + "/" + endpoint
    file_name = endpoint

    if args:
        url += "?"
        url += urllib.parse.urlencode(args, safe=",")

        file_name += "_"
        file_name += hashlib.md5(str(args).encode()).hexdigest()

        if "format" in args:
            file_name += "." + args["format"]

    return (url, file_name)


def _validate_date(date: str | datetime.datetime) -> str:
    if isinstance(date, str) and date == "-today":
        date = datetime.datetime.today()

    if isinstance(date, datetime.datetime):
        date = date.strftime("%Y-%m-%d")

    # ENHANCEMENT: accept other date formats like numpy datetime64, pandas Timestamp, etc
    # ENHANCEMENT: make sure date is properly formatted

    return date


def get_model_version() -> str:
    """Get the current default model version.

    Returns:
        str: The current model version

    """
    return MODEL_VERSION


def set_model_version(version: str) -> None:
    """Set the default model version.

    Args:
        version (str): The model version to set

    """
    assert version in MODEL_VERSIONS
    global MODEL_VERSION
    MODEL_VERSION = version


def get_current_session() -> None | requests.Session:
    """Get the current session.

    Returns:
        None | requests.Session: The current session

    """
    return CURRENT_SESSION


def set_current_session(session: requests.Session) -> None:
    """Set the current session.

    Args:
        session (requests.Session): The session to set

    """
    global CURRENT_SESSION
    CURRENT_SESSION = session
