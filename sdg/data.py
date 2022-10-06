# -*- coding: utf-8 -*-
"""
Output the data in a variety of formats

@author: dashton
"""
import pandas as pd
import os
from sdg.path import output_path, input_path


def get_inid_data(inid, src_dir=''):
    pth = input_path(inid, ftype='data', src_dir=src_dir, must_work=True)
    df = pd.read_csv(pth)
    return df


def filter_headline(df, non_disaggregation_columns):
    """Given a dataframe filter it down to just the headline data.

    In the case of multiple units it will keep all headline for each unit.
    """

    special_cols = [col for col in non_disaggregation_columns if col in df.columns]

    # Select the non-data rows and filter rows that are all missing (nan)
    disag = df.drop(special_cols, axis=1)
    headline_rows = disag.isnull().all(axis=1)

    headline = df.filter(special_cols, axis=1)[headline_rows]

    return headline


def write_csv(inid, df, ftype='data', site_dir=''):
    """
    For a given ID and data set, write out as csv

    Args:
        inid: str. The indicator identifier
        df: DataFrame. The pandas data frame of the data
        ftype: Sets directory path
        site_dir: str. The site directory to build to.

    Returns:
        bool: Status
    """
    status = True

    # If the csv dir isn't there, make it
    csv_dir = output_path(ftype=ftype, format='csv', site_dir=site_dir)
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir, exist_ok=True)

    # The path within the csv dir
    out_path = output_path(inid,  ftype=ftype, format='csv', site_dir=site_dir)

    try:
        df.to_csv(out_path, index=False, encoding='utf-8-sig')
    except Exception as e:
        print(inid, e)
        return False

    return status

