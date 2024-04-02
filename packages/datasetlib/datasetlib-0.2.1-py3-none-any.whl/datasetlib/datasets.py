# =============================================================================
#
#  Licensed Materials, Property of Ralph Vogl, Munich
#
#  Project : basefunctions
#
#  Copyright (c) by Ralph Vogl
#
#  All rights reserved.
#
#  Description:
#
#  datasets provide basic access to well known datasets used for machine learning
#
# =============================================================================

# -------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------
import os

import basefunctions as bf
import pandas as pd

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS REGISTRY
# -------------------------------------------------------------

# -------------------------------------------------------------
# DEFINITIONS
# -------------------------------------------------------------
_dataset_dict = {
    "aapl": (
        "datasets/apple.csv",
        {"index_col": [0], "parse_dates": [0], "header": [0]},
    ),
    "babynames": ("datasets/babynames.csv", {"index_col": [0]}),
    "bmw": ("datasets/bmw.csv", {"index_col": [0], "parse_dates": [0], "header": [0]}),
    "summergames": ("datasets/summergames.csv", {"index_col": [0], "header": [0]}),
    "titanic": ("datasets/titanic.csv", {}),
}


# -------------------------------------------------------------
# VARIABLE DEFINTIONS
# -------------------------------------------------------------


# -------------------------------------------------------------
# FUNCTION DEFINTIONS
# -------------------------------------------------------------
def get_datasets():
    """get a list of all available datasets

    Returns
    -------
    list
        list of available datasets
    """
    return list(_dataset_dict.keys())


def get_dataset_filename(dataset_name):
    """get the filename for a specific dataset

    Parameters
    ----------
    dataset_name : str
        name of dataset

    Returns
    -------
    str
        file name of dataset

    Raises
    ------
    RuntimeError
        raises RuntimeError if dataset name can't be found
    """
    print(
        os.path.sep.join(
            [bf.get_path_name(os.path.abspath(__file__)), _dataset_dict[dataset_name][0]]
        )
    )
    if dataset_name in _dataset_dict:
        return bf.norm_path(
            os.path.sep.join(
                [
                    bf.get_path_name(os.path.abspath(__file__)),
                    _dataset_dict[dataset_name][0],
                ]
            )
        )
    else:
        raise RuntimeError(f"dataset {dataset_name} not found")


def get_dataset(dataset_name):
    """get a specific dataset

    Parameters
    ----------
    dataset_name : str
        name of dataset

    Returns
    -------
    pandas dataframe
        dataframe of dataset

    Raises
    ------
    RuntimeError
        raises RuntimeError if dataset name can't be found
    """
    if dataset_name in _dataset_dict:
        _, kwargs = _dataset_dict[dataset_name]
        return pd.read_csv(get_dataset_filename(dataset_name), **kwargs)
    else:
        raise RuntimeError(f"dataset {dataset_name} not found")
