# -*- coding: utf-8 -*-
"""

@author: Daniel Stepanek
"""


import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

from file_processing import get_data
      
        
"""
    For each experiment plot data in one figure.
"""
def plot_data(fig_location: str = None):
    
        
    for file, data in get_data():
        fig, axs = plt.subplots(nrows=5, ncols=1, sharex=True,
                           constrained_layout=True, figsize=(16, 9))
        
        fig.suptitle('Fyziologicka data')
    
        bvp = data['bvp']
        gsr = data['gsr']
        hr = data['hr']
        temp = data['temp']
        tag = data['tag']
        
        axs[0].plot(bvp['norm_ts'], bvp['value'])
        axs[0].set_ylabel('BVP')
        axs[0].set_yticks(np.arange(-600, 600, 200))  
        
        axs[1].plot(gsr['norm_ts'], gsr['value'])
        axs[1].set_ylabel('GSR')
        axs[1].set_yticks(np.arange(0, 6, 1))
        
        axs[2].plot(hr['norm_ts'], hr['value'])
        axs[2].set_ylabel('HR')
        axs[2].set_yticks(np.arange(50, 120, 10))
        
        axs[3].plot(temp['norm_ts'], temp['value'])
        axs[3].set_ylabel('Temperature')
        axs[3].set_yticks(np.arange(30, 38, 1))
        
        tag['value'] = 1
        axs[4].scatter(tag['norm_ts'], tag['value'])
        axs[4].set_ylabel('Tag')
        axs[4].set_yticks(np.arange(0, 2, 0.5))
        
        if fig_location:
            plt.savefig('{}/{}.png'.format(fig_location, file))
        

if __name__ == '__main__':
    path = '.\\plots'
    p = Path(path)
    p.mkdir(exist_ok=True)
        
    plot_data(fig_location=path)
    
    