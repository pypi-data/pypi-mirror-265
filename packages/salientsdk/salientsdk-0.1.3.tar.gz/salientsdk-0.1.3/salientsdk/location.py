#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Define the Location class."""

# Usage example:
# python location.py --lat 42 --lon -73

import argparse
import datetime
import os
import urllib

from . import constants, login_api


class Location:
    """Define geographical parameters for an API query.

    The Salient API
    can define location by a single latitude/longitude, multiple
    latitude/longitude pairs in a single location_file, or a polygon
    defined in a shapefile.
    """

    def __init__(
        self,
        lat: float | None = None,
        lon: float | None = None,
        location_file: str | None = None,
        shapefile: str | None = None,
    ):
        """Initialize a Location object.

        Only one of the following 3 options should be used at a time: lat/lon,
        location_file, or shapefile.

        Args:
            lat (float): Latitude in degrees, -90 to 90.
            lon (float): Longitude in degrees, -180 to 180.
            location_file (str): Path to a CSV file with latitude and longitude columns.
            shapefile (str): Path to a shapefile with a polygon defining the location.
        """
        self.lat = lat
        self.lon = lon
        self.location_file = location_file
        self.shapefile = shapefile

        self.__validate()

    @staticmethod
    def _from_args_(args: argparse.Namespace) -> "Location":
        """Parse command line arguments.

        Factory method that builds a `Location` object from an argument
        parser of the type returned by `get_argparser`.
        """
        return Location(
            lat=args.latitude,
            lon=args.longitude,
            location_file=args.location_file,
            shapefile=args.shapefile,
        )

    @staticmethod
    def get_argparser(args: list[str] = [], login_args=True) -> argparse.ArgumentParser:
        """Generate an argument parser that parses Location-specific arguments.

        Args:
            args (list[str]): Additional standard/shared arguments to add to the parser.
            login_args (bool): If True (default), add standard login arguments
                of `username`, `password`, `verify`, and `verbose`.

        Generate an argument parser for the Location class with consistent arguments
        that can be used across multiple `main()` functions and the command line.
        """
        argparser = argparse.ArgumentParser()
        argparser.add_argument("-lat", "--latitude", type=float, default=None)
        argparser.add_argument("-lon", "--longitude", type=float, default=None)
        argparser.add_argument("-loc", "--location_file", type=str, default=None)
        argparser.add_argument("-shp", "--shapefile", type=str, default=None)

        if login_args:
            argparser = login_api._add_login_args(argparser)

        if "debias" in args:
            argparser.add_argument("--debias", type=bool, default=False)

        if "version" in args:
            argparser.add_argument("-ver", "--version", type=str, default=constants.MODEL_VERSION)

        if "force" in args:
            argparser.add_argument("--force", type=bool, default=False)

        if "verbose" in args:
            argparser.add_argument("--verbose", type=bool, default=True)

        if "date" in args:
            argparser.add_argument("--date", type=str, default="-today")

        return argparser

    def asdict(self, **kwargs) -> dict:
        """Render as a dictionary.

        Generates a dictionary representation that can be encoded into a URL.
        Will contain one and only one location_file, shapefile, or lat/lon pair.

        Args:
            **kwargs: Additional key-value pairs to include in the dictionary.
                Will validate some common arguments that are shared across API calls.
        """
        if self.location_file:
            dct = {"location_file": self.location_file, **kwargs}
        elif self.shapefile:
            dct = {"shapefile": self.shapefile, **kwargs}
        else:
            dct = {"lat": self.lat, "lon": self.lon, **kwargs}

        if "apikey" in dct:
            assert (
                isinstance(dct["apikey"], str) & len(dct["apikey"]) > 0
            ), "API key must be a string"

        if "start" in dct:
            dct["start"] = constants._validate_date(dct["start"])
        if "end" in dct:
            dct["end"] = constants._validate_date(dct["end"])
        if "forecast_date" in dct:
            dct["forecast_date"] = constants._validate_date(dct["forecast_date"])

        if "version" in dct:
            assert (
                dct["version"] in constants.MODEL_VERSIONS
            ), f"Version {dct['version']} not in {constants.MODEL_VERSIONS}"

        if "shapefile" in dct and "debias" in dct and dct["debias"]:
            raise ValueError("Cannot debias with shapefile locations")

        return dct

    def asargs(self, **kwargs) -> str:
        """Render as api arguments.

        Encodes a dictionary of the type returned by `asdict` into a
        single string appropriate for an API request.
        """
        return urllib.parse.urlencode(self.asdict(**kwargs), safe=",")

    def __validate(self):
        if self.location_file:
            assert os.path.exists(
                self.location_file
            ), f"Location file {self.location_file} does not exist"
            assert not self.lat, "Cannot specify both lat and location_file"
            assert not self.lon, "Cannot specify both lon and location_file"
            assert not self.shapefile, "Cannot specify both shape_file and location_file"
        elif self.shapefile:
            assert os.path.exists(self.shapefile), f"Shape file {self.shapefile} does not exist"
            assert not self.lat, "Cannot specify both lat and shape_file"
            assert not self.lon, "Cannot specify both lon and shape_file"
        else:
            assert self.lat, "Must specify lat & lon or location_file or shape_file"
            assert self.lon, "Must specify lat & lon or location_file or shape_file"
            assert -90 <= self.lat <= 90, "Latitude must be between -90 and 90 degrees"
            assert -180 <= self.lon <= 180, "Longitude must be between -180 and 180 degrees"

    def __str__(self):
        """Return a string representation of the Location object."""
        if self.location_file:
            return f"location file: {self.location_file}"
        elif self.shapefile:
            return f"shape file: {self.shapefile}"
        else:
            return f"({self.lat}, {self.lon})"

    def __eq__(self, other):
        """Check if two Location objects are equal."""
        if self.location_file:
            return self.location_file == other.location_file
        elif self.shapefile:
            return self.shapefile == other.shape_file
        else:
            return self.lat == other.lat and self.lon == other.lon

    def __ne__(self, other):
        """Check if two Location objects are not equal."""
        return not self.__eq__(other)


if __name__ == "__main__":
    argparser = Location.get_argparser()
    args = argparser.parse_args()
    location = Location._from_args_(args)

    print(location)
    print(location.asdict(foo="bar"))
