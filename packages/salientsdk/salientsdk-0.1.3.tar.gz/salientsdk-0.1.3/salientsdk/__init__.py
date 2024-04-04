#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Salient Predictions Software Development Kit."""

import os

import toml

from .constants import get_model_version, set_model_version
from .data_timeseries_api import data_timeseries, load_multihistory
from .downscale_api import downscale
from .forecast_timeseries_api import forecast_timeseries
from .location import Location
from .login_api import login
from .upload_file_api import upload_bounding_box, upload_file, upload_location_file

init_file_dir = os.path.dirname(__file__)
pyproject_path = os.path.join(init_file_dir, "..", "pyproject.toml")

with open(pyproject_path) as f:
    pyprj = toml.load(f)
    prj = pyprj["tool"]["poetry"]

__version__ = prj["version"]
__author__ = "Salient Predictions"
__all__ = [
    "login",
    "data_timeseries",
    "downscale",
    "forecast_timeseries",
    "get_model_version",
    "load_multihistory",
    "Location",
    "set_model_version",
    "upload_file",
    "upload_bounding_box",
    "upload_location_file",
]

if __name__ == "__main__":
    print(f"ver: {__version__} by: {__author__}")
