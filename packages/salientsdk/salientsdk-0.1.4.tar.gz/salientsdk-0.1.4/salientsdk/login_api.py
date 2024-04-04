#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Login to the Salient API.

Command line usage:
```
cd ~/salientsdk
python -m salientsdk login -u testusr -p testpwd
```

"""

import argparse

import requests

from .constants import _build_url

try:
    from google.cloud import secretmanager
except ImportError as ie:
    # secretmanager is a convenience for internal Salient users.
    # Not needed for customer use.
    pass


VERFY_SSL = True

CURRENT_SESSION = None


def get_current_session() -> None | requests.Session:
    """Get the current session.

    All calls to the Salient API have a `session` argument
    that defaults to call this function. In most cases, users
    will never need to call it explicitly.

    Returns:
        None | requests.Session: The current session

    """
    return CURRENT_SESSION


def set_current_session(session: requests.Session) -> None:
    """Set the current session.

    This function is called internally as a side effect of
    `login()`. In most cases, users will never need
    to call it explicitly.

    Args:
        session (requests.Session): The session that will be
              returned by `get_current_session()`

    """
    global CURRENT_SESSION
    CURRENT_SESSION = session


def get_verify_ssl() -> bool:
    """Get the current SSL verification setting.

    All functions that call the Salient API have a
    `verify` argument that controls whether or not to use
    SSL verification when making the call.  That argument
    will default to use this function, so in most cases
    users will never need to call it.

    Returns:
        bool: The current SSL verification setting

    """
    return VERFY_SSL


def set_verify_ssl(verify: bool) -> None:
    """Set the SSL verification setting.

    Sets the default value to be used when calling
    `verify = get_verify_ssl()` in most API calls.
    This is usually set automatically as a side
    effect of `login(..., verify=None)` so in most
    cases users will never need to call it.

    Args:
        verify (bool): The SSL verification setting
           that will be returned by `get_verify_ssl()`.

    """
    global VERFY_SSL
    VERFY_SSL = verify


def login(
    username: str = "username",
    password: str = "password",
    verify: bool | None = None,
    verbose=False,
) -> requests.Session:
    """Login to the Salient API.

    This function is a local convenience wrapper around the Salient API
    [login](https://api.salientpredictions.com/v2/documentation/api/#/Authentication/login)
    endpoint.  It will use your credentials to create a persistent session you
    can use to execute API calls.

    Args:
        username (str): The username to login with
        password (str): The password to login with
        verify (bool): Whether to verify the SSL certificate.
           If `None` (default) will try `True` and then `False`, remembering the
           last successful setting and preserving it for future calls in `get_verify_ssl()`.
        verbose (bool): Whether to print the response status

    Returns:
        session: object to pass to other API calls.  As a side effect, will also set
           the current session for use with `get_current_session()`
    """
    if username == "username" and password == "password":
        password_path = "projects/forecast-161702/secrets/API_TEST_USER_PWD/versions/1"
        username = "testuser@salientpredictions.com"
        try:
            password = (
                secretmanager.SecretManagerServiceClient()
                .access_secret_version(request={"name": password_path})
                .payload.data.decode("UTF-8")
            )
        except Exception as e:
            raise ValueError("Supply your Salient username and password")
    elif username == "testusr" and password == "testpwd":
        username = "help+test@salientpredictions.com"
        password = "salty!"

    if verify is None:
        try:
            session = login(username, password, verify=True, verbose=verbose)
            set_verify_ssl(True)
        except requests.exceptions.SSLError:
            session = login(username, password, verify=False, verbose=verbose)
            set_verify_ssl(False)
        return session

    auth = (username, password)
    (url, file_name) = _build_url("login")

    session = requests.Session()
    login_ok = session.get(url, auth=auth, verify=verify)
    login_ok.raise_for_status()

    if verbose:
        print(login_ok.text)

    set_current_session(session)

    return session
