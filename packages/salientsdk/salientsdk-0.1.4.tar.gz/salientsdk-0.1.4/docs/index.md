
# Intended Use

The Salient SDK is a python convenience wrapper around Salient Predictions' customer-facing  
[web API](https://api.salientpredictions.com/v2/documentation/api/).  It also contains utility functions for manipulating and analyzing the data delivered from the API.

# Setting up the SDK

## Prerequisites 

The Salient SDK requires Python 3.11 to use.   If you have Python installed, you can check your version with:

```bash
python3 --version
```

To get version 3.11:

```bash
# Ubuntu:
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
```

```bash
# macOS:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update
brew install python@3.11
```

## Installing the SDK

The easiest way to get the Salient SDK is to install it like any other package:

```bash
pip install salientsdk --upgrade
# to verify version with
pip show salientsdk
```

# Usage

## Command Line

The Salient SDK contains a full command line interface that can access each of the primary
API functions without even opening python.  You can get help for all options or specific commands:

```bash
python3 -m salientsdk --help
python3 -m salientsdk forecast_timeseries --help
```

To access the Salient API you will need a `username` and `password` provided by
your Salient representative.  The universal credentials `testusr` and `testpwd` 
have limited permissions for testing and validation purposes:

```bash
python3 -m salientsdk data_timeseries -lat 42 -lon -73 -fld all --start 2020-01-01 --end 2020-12-31 -u testusr -p testpwd
```

## Via Python

In a python 3.11 script, this example code will login and request a historical ERA5 data timeseries.

```python
import salientsdk as sk
import xarray as xr
import netcdf4

session = sk.login("testusr","testpwd")
history = sk.data_timeseries(loc = Location(lat=42, lon=-73), field="all", variable="temp", session=session)
print(xr.open_file(history))
```

Note that this example uses the limited credentials `testusr` and `testpwd`.  To access the full capabilities of your license, use your Salient-provided credentials.

See all available functions in the [API Reference](api.md).

The [examples](https://github.com/Salient-Predictions/salientsdk/tree/main/examples) directory contains `ipynb` notebooks to help you get started with common operations. 

# License

This SDK is licensed for use by Salient customers [details](https://salient-predictions.github.io/salientsdk/LICENSE/).


Copyright 2024 [Salient Predictions](https://www.salientpredictions.com/)
