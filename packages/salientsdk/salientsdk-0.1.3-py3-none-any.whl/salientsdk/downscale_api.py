#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Interface to the Salient data_timeseries API.

Command line usage example:
```
cd ~/salientsdk
python -m salientsdk.downscale_api -lat 42 -lon -73 --date 2020-01-01
```

"""

import os
from datetime import datetime

import requests
import xarray as xr

from . import constants, location, login_api


def downscale(
    loc: location.Location,
    variables: str = "temp,precip",
    debias: bool = False,
    date: str = "-today",
    members: int = 50,
    version: str = constants.get_model_version(),
    force: bool = False,
    session: requests.Session = constants.get_current_session(),
    verify: bool = constants.VERFY_SSL,
    verbose: bool = False,
    **kwargs,
) -> str | list[str]:
    """Temporal downscale of forecasts.

    Convert temporally coarse probabilistic forecasts into granular daily ensembles.
    For more detail, see the
    [api doc](https://api.salientpredictions.com/v2/documentation/api/#/Forecasts/downscale).

    Args:
        loc (Location): The location to query
        variables (str): The variables to query, separated by commas
            See the
            [Data Fields](https://salientpredictions.notion.site/Variables-d88463032846402e80c9c0972412fe60)
            documentation for a full list of available variables.
        date (str): The start date of the time series.
        members (int): The number of ensemble members to download
        debias (bool): If True, debias the data
        version (str): The model version of the Salient `blend` forecast.
        force (bool): If False (default), don't download the data if it already exists
        session (requests.Session): The session object to use for the request
        verify (bool): If True (default), verify the SSL certificate
        verbose (bool): If True (default False) print status messages
        **kwargs: Additional arguments to pass to the API

    Keyword Arguments:
        gdd_base (int): The base temperature for growing degree days
        units (str): US or SI

    Returns:
        str: the name of the downloaded (or cached) downscale data file
    """
    format = "nc"
    frequency = "daily"
    model = "blend"

    assert members > 0, "members must be a positive integer"
    assert isinstance(session, requests.Session), "Must login to the Salient API first"

    if date == "-today":
        date = datetime.today().strftime("%Y-%m-%d")

    endpoint = "downscale"
    args = loc.asdict(
        variables=variables,
        date=date,
        debias=debias,
        members=members,
        format=format,
        model=model,
        version=version,
        frequency=frequency,
        **kwargs,
    )

    (query, file_name) = constants._build_url(endpoint, args)

    if force or not os.path.exists(file_name):
        if verbose:
            print(f"Downloading {query} to {file_name}")
        with open(file_name, "wb" if format == "nc" else "w") as f:
            result = session.get(query, verify=verify)
            result.raise_for_status()
            if format == "nc":
                f.write(result.content)
            else:
                f.write(result.text)
    elif verbose:
        print(f"File {file_name} already exists")

    return file_name


def _main():
    argparser = location.Location.get_argparser(["date", "debias", "version", "force"])
    argparser.add_argument("-var", "--variables", type=str, default="temp,precip")
    argparser.add_argument("--members", type=int, default=50)
    # These are currently the only available values.  Not necessary to expose
    # these as options from the command line.
    # argparser.add_argument("--format", type=str, default="nc")
    # argparser.add_argument("--frequency", type=str, default="daily")

    args = argparser.parse_args()

    session = login_api._login_from_args(args)

    loc = location.Location._from_args_(args)
    file_name = downscale(
        loc,
        variables=args.variables,
        debias=args.debias,
        date=args.date,
        members=args.members,
        version=args.version,
        # format=args.format,
        # frequency=args.frequency,
        force=args.force,
        verbose=args.verbose,
        session=session,
    )

    if args.verbose:
        print(xr.open_dataset(file_name))


if __name__ == "__main__":
    _main()
