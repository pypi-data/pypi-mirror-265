
# Intended Use

The Salient SDK is a convenience wrapper around Salient Predictions' customer-facing  
[web API](https://api.salientpredictions.com/v2/documentation/api/).  It also contains utility functions for manipulating and analyzing the data delivered from the API.

# Setting up the SDK

## Prerequisites 

The Salient SDK requires Python 3.11 to use.   If you have Python installed, you can check your version with:

```bash
python --version
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
pip install salientsdk
```







# Usage

To access the Salient API you will need a `username` and `password` provided by
your Salient representative.  The universal credentials `testusr` and `testpwd` 
have limited permissions for testing and validation purposes:

```bash
python -m salientsdk.data_timeseries -lat 42 -lon -73 -fld all --start 2020-01-01 --end 2020-12-31 -u testusr -p testpwd
```

In a python script:

```python
import salientsdk as sk
import xarray as xr
import netcdf4

session = sk.login("testusr","testpwd")
history = sk.data_timeseries(loc = Location(lat=42, lon=-73), field="all", variable="temp")
print(xr.open_file(history))
```

See all available functions in the [API Reference](api.md).

The [examples](https://github.com/Salient-Predictions/salientsdk/tree/main/examples) directory contains `ipynb` notebooks to help you get started with common operations. 

# License

This SDK is licensed for use by Salient customers [details](LICENSE.md).


Copyright 2024 [Salient Predictions](https://www.salientpredictions.com/)
