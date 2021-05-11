# -*- coding: utf-8 -*-
"""
 Project: Bachelor thesis
 Theme: Physiological Data to Analyze and Improve the User Experience
 Author: Daniel Stepanek
 License: GPL 3.0

 VUT FIT Brno 2021

"""

import os
import pandas as pd

def load_files(folder, extension="txt"):
    """
    Get all files from folder with specific extension.

    Parameters
    ----------

    folder : str
        Folder path.

    extension : str
        Type of file which will be loaded.

    Returns
    -------
    list : List of loaded files.

    """

    files = []
    for file in os.listdir(folder):
        if os.path.splitext(file)[1] == '.{}'.format(extension):
            files += [file]
    return files

def get_all_data(path='./data'):
    """
    Generate data from csv files of all sessions.

    Parameters
    ----------

    path : str
        Specify the path where the data folders will be searched.

    Returns
    -------
    Iterator : Yield folder name and data from the folder.

    """

    folders = os.listdir(path)
    for folder in folders:
        folder_path = '{}/{}'.format(path, folder)
        data = get_data(folder_path)
        yield folder, data

def get_data(folder_path):
    """
    Get data from csv files of session.

    Parameters
    ----------

    folder_path : str
        Data folder path.

    Returns
    -------
    dict : Dict of E4 data (DataFrames) from folder.

    """

    if not os.path.isdir(folder_path):
        return None

    bvp = pd.read_csv('{}/raw/E4_Bvp.csv'.format(folder_path))
    gsr = pd.read_csv('{}/raw/E4_Gsr.csv'.format(folder_path))
    hr = pd.read_csv('{}/raw/E4_Hr.csv'.format(folder_path))
    ibi = pd.read_csv('{}/raw/E4_Ibi.csv'.format(folder_path))
    temp = pd.read_csv('{}/raw/E4_Temperature.csv'.format(folder_path))
    tag = pd.read_csv('{}/raw/E4_Tag.csv'.format(folder_path))

    data = {'bvp' : bvp,
            'gsr' : gsr,
            'hr' : hr,
            'ibi' : ibi,
            'temp' : temp,
            'tag' : tag}

    return data
