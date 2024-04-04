#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Login to the Salient API."""

import argparse

import requests

from . import constants

try:
    from google.cloud import secretmanager
except ImportError as ie:
    # secretmanager is a convenience for internal Salient users.
    # Not needed for customer use.
    pass


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
        verify (bool): Whether to verify the SSL certificate
        verbose (bool): Whether to print the response status

    Returns:
        session: object to pass to other API calls
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
            session = login(username, password, True, verbose)
            constants.VERFY_SSL = True
        except requests.exceptions.SSLError:
            session = login(username, password, False, verbose)
            constants.VERFY_SSL = False
        return session

    auth = (username, password)
    (url, file_name) = constants._build_url("login")

    session = requests.Session()
    login_ok = session.get(url, auth=auth, verify=verify)
    login_ok.raise_for_status()

    if verbose:
        print(login_ok.text)

    constants.set_current_session(session)

    return session


def _login_from_args(args: argparse.Namespace) -> requests.Session:
    """Dispatch login from argparse arguments.

    Args:
        args: argparse.Namespace object

    Returns:
        session: object to pass to other API calls
    """
    assert hasattr(args, "username")
    assert hasattr(args, "password")
    assert hasattr(args, "verify")
    assert hasattr(args, "verbose")

    return login(args.username, args.password, args.verify, args.verbose)


def _add_login_args(
    args: argparse.ArgumentParser = argparse.ArgumentParser(),
) -> argparse.ArgumentParser:
    """Add login arguments to an argparse.ArgumentParser.

    Args:
        args: argparse.ArgumentParser object.  Creates one if not provided.

    Returns:
        args: argparse.ArgumentParser object with login arguments for
            `username`, `password`, `verify`, and `verbose`
    """
    args.add_argument("-u", "--username", type=str, default="username")
    args.add_argument("-p", "--password", type=str, default="password")
    args.add_argument("--verify", type=bool, default=None)
    args.add_argument("--verbose", type=bool, default=True)

    return args


if __name__ == "__main__":
    args = _add_login_args().parse_args()
    session = _login_from_args(args)

    if args.verbose:
        print(session)
