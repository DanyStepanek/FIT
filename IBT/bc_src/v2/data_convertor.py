# -*- coding: utf-8 -*-
"""

@author: Daniel Stepanek
"""


import os
import pandas as pd
import numpy as np
from pathlib import Path

from file_processing import load_files

"""
    Convert txt file to dataframes and
    save to csv files named by data subscriptions.
"""
def raw_data_to_csv(files, path, keep_raw_data=False):
    for file in files:

        new_folder =  '{}\\{}'.format(path, file.split('.')[0])
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
        with open('{}\\{}'.format(path, file), 'r') as f:
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

        p = Path('{}\\raw'.format(new_folder))
        p.mkdir(exist_ok=True)

        #create dataframe and save to csv
        for key in data_dict.keys():
            df = pd.DataFrame(data_dict[key])
            df['norm_ts'] = None
            df['norm_ts'] = df['timestamp'].astype('float') - zero_time

            df['value'] = df['value'].astype(float)
            df['timestamp'] = df['timestamp'].astype(float)

            df.to_csv(r'{}\\{}.csv'.format(p, key),
                                        index=False, header=True)

        if not keep_raw_data:
            os.remove('{}\\{}'.format(path, file))


if __name__ == '__main__':
    path = '.\\data'
    files = load_files(path)
    raw_data_to_csv(files, path)
