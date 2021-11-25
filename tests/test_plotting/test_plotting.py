"""Tests the generation of data for the plot."""
import os
import pickle
from distutils import dir_util

import pandas as pd
import pytest

from lbpackages.plotting import plotting


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


# Simulates grouped DataFrames
@pytest.fixture
def sim_df():
    """Creates the necesary pandas object to run the tests."""
    case_A = pd.DataFrame(
        [
            "GOOG",
            "AMZN",
            "MSFT",
            "WMT",
            "HD",
            "CVH",
            "AXP",
            "BA",
            "MRK",
            "JNJ",
            "DIS",
        ],
        columns=["symbol"],
    ).groupby("symbol")
    case_B = pd.DataFrame(
        ["AXP", "BA", "MRK", "JNJ", "DIS"], columns=["symbol"]
    ).groupby("symbol")
    case_C = pd.DataFrame(["WMT", "HD", "CVH"], columns=["symbol"]).groupby("symbol")
    case_D = pd.DataFrame(["GOOG", "AMZN", "MSFT"], columns=["symbol"]).groupby(
        "symbol"
    )
    return {"A": case_A, "B": case_B, "C": case_C, "D": case_D}


@pytest.fixture
def dates():
    """The dates for the test."""
    return {"A": "2021-10-15", "B": "2021-10-15", "C": "2021-11-05", "D": "2021-11-05"}


# Expected output already saved in .pkl files.
@pytest.fixture
def exp_menu(datadir):
    """Reads the expected output from files."""
    exp_menu_dict = {}
    ls = os.listdir(datadir)
    for file in os.listdir(datadir):
        if ".pkl" in file:
            case = file[0]
            fn = os.path.join(datadir, file)
            with open(fn, "rb") as f:
                exp = pickle.load(f)
            exp_menu_dict[case] = exp
    return exp_menu_dict


# Test for the method that generates the list to create an update_menu object.
def test_update_menus(sim_df, dates, exp_menu):
    for case in ["A", "B", "C", "D"]:
        grouped_df = sim_df[case]
        ds = dates[case]
        exp = exp_menu[case]
        actual_menu = plotting.create_update_menu(grouped_df, ds)
        assert actual_menu == exp
