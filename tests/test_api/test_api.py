"""Tests format data fetched from API."""
import os
import pickle
from distutils import dir_util

import pandas as pd
import pytest

from lbpackages.get_data import get_data


@pytest.fixture
def datadir(tmpdir, request):
    """
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    """
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


# Mocks API Response
@pytest.fixture
def api_mock(datadir):
    """Mocks the API response."""
    api_resp_dict = {}

    for file in os.listdir(datadir):
        if ".pkl" in file:
            ticker = file[:3]
            fn = os.path.join(datadir, file)
            with open(fn, "rb") as f:
                api_resp = pickle.load(f)
            api_resp_dict[ticker] = api_resp
    return api_resp_dict


# Expected output already saved in .csv files.
@pytest.fixture
def exp_df(datadir):
    """Reads from file the expected response for the test."""
    exp_df_dict = {"IBM": {}, "OIH": {}}

    for file in os.listdir(datadir):
        if ".csv" in file:
            ticker = file[:3]
            date = file[3:13]
            fn = os.path.join(datadir, file)
            exp_df = pd.read_csv(fn, header=None, dtype="str")
            exp_df_dict[ticker][date] = exp_df
    return exp_df_dict


@pytest.fixture
def tickers():
    """The tickers for the test."""
    return ["IBM", "OIH"]


@pytest.fixture
def dates():
    """The dates for the test."""
    return ["2021-10-15", "2021-11-05"]


# Tests formatting method from the class against expected output.
def test_df(tickers, dates, api_mock, exp_df):
    """Process data and compares it againt expected output."""
    api_client = get_data.StocksApiClient("")

    for ticker in tickers:
        for date in dates:

            api_client.raw = api_mock[ticker]
            df_actual = api_client._format_data(ticker, date)
            pd.testing.assert_frame_equal(df_actual, exp_df[ticker][date])
