# -*- coding: utf-8 -*-
"""

@author: Daniel Stepanek
"""

import os
import pandas as pd

"""
    Get all files from folder with specific extension.
"""
def load_files(folder, extension="txt"):
    files = []
    for file in os.listdir(folder):
        if os.path.splitext(file)[1] == f'.{extension}':
            files += [file]
    return files
    
"""
    Generate data from csv files of sessions.
"""
def get_data(path='.\\data'):
        folders = os.listdir(path)
        
        for folder in folders:
            folder_path = '{}/{}'.format(path, folder)
            if not os.path.isdir(folder_path):
                continue
         
            bvp = pd.read_csv('{}/E4_Bvp.csv'.format(folder_path))
            gsr = pd.read_csv('{}/E4_Gsr.csv'.format(folder_path))
            hr = pd.read_csv('{}/E4_Hr.csv'.format(folder_path))
            ibi = pd.read_csv('{}/E4_Ibi.csv'.format(folder_path))
            temp = pd.read_csv('{}/E4_Temperature.csv'.format(folder_path))
            tag = pd.read_csv('{}/E4_Tag.csv'.format(folder_path))
            
            data = {'bvp' : bvp,
                    'gsr' : gsr,
                    'hr' : hr,
                    'ibi' : ibi,
                    'temp' : temp,
                    'tag' : tag}
                   
            yield folder, data
            
            