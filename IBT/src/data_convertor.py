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
import numpy as np
from pathlib import Path

from file_processing import load_files

def raw_data_to_csv(files, path, keep_raw_data=False):
    """
    Convert txt file to dataframes and
    save them as csv files named by data subscriptions (signal type).

    Parameters
    ----------

    files : list
        List of txt files containing raw data.

    path : str
        Path where data are stored and csv files will be stored.

    keep_raw_data: bool
        If set, keep txt files with raw data.

    """

    for file in files:
        new_folder =  '{}/{}'.format(path, file.split('.')[0])
        p = Path(new_folder)
        p.mkdir(exist_ok=True)

        keys = ['E4_Bvp', 'E4_Temperature', 'E4_Hr',
                'E4_Ibi', 'E4_Gsr', 'E4_Tag']
        data_dict = dict.fromkeys(keys)

        #create dict with subdicts timestamp, value
        for key in keys:
            data_dict[key] = dict.fromkeys(['timestamp', 'value'])
            data_dict[key]['timestamp'] = []
            data_dict[key]['value'] = []


        #get data from txt file
        with open('{}/{}'.format(path, file), 'r') as f:
            data = f.read()

        data = data.splitlines()

        #first timestamp for all csv
        zero_time = np.inf

        #parse data to dict
        for d in data:
            d_split = d.split(' ')

            #internal response  handler
            if d_split[0] == 'R':
                print('Session info: {}'.format(d))
                continue

            #find the first timestamp to normalize timestamps in all csv
            ts = float(d_split[1])
            if ts < zero_time:
                zero_time = ts

            data_dict[d_split[0]]['timestamp'] += [d_split[1]]
            data_dict[d_split[0]]['value'] += [d_split[2]]

        p = Path('{}/raw'.format(new_folder))
        p.mkdir(exist_ok=True)

        #create dataframe and save as csv
        for key in data_dict.keys():
            df = pd.DataFrame(data_dict[key])
            df['norm_ts'] = None
            df['norm_ts'] = df['timestamp'].astype('float') - zero_time

            df['value'] = df['value'].astype(float)
            df['timestamp'] = df['timestamp'].astype(float)

            df.to_csv(r'{}/{}.csv'.format(p, key),
                                        index=False, header=True)

        if not keep_raw_data:
            os.remove('{}/{}'.format(path, file))


if __name__ == '__main__':
    path = os.path.dirname(os.getcwd())
    path = '{}/data'.format(path)

    files = load_files(path)
    raw_data_to_csv(files, path)
