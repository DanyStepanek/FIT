# -*- coding: utf-8 -*-
"""
 Project: Bachelor thesis
 Theme: Physiological Data to Analyze and Improve the User Experience
 Author: Daniel Stepanek
 License: GPL 3.0

 VUT FIT Brno 2021

"""


import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import os

from file_processing import get_all_data


def plot_data(fig_location=None):
    """
    For each stimuli plot data in one figure.

    Parameters
    ----------

    fig_location : str
        Specify, where plots should be stored.
    """


    for file, data in get_all_data():
        fig, axs = plt.subplots(nrows=6, ncols=1, sharex=True,
                           constrained_layout=True, figsize=(16, 9))

        fig.suptitle('Fyziologická data')

        bvp = data['bvp']
        gsr = data['gsr']
        hr = data['hr']
        ibi = data['ibi']
        temp = data['temp']
        tag = data['tag']

        axs[0].plot(bvp['norm_ts'], bvp['value'])
        axs[0].set_xlabel('Čas [s]')
        axs[0].set_ylabel('PPG signál [nW]')

        axs[1].plot(gsr['norm_ts'], gsr['value'])
        axs[1].set_xlabel('Čas [s]')
        axs[1].set_ylabel('EDA signál [uS]')

        axs[2].plot(hr['norm_ts'], hr['value'])
        axs[2].set_xlabel('Čas [s]')
        axs[2].set_ylabel('Srdeční tep [úderů/min]')

        axs[3].plot(ibi['norm_ts'], ibi['value'])
        axs[3].set_xlabel('Čas [s]')
        axs[3].set_ylabel('IBI [s]')

        axs[4].plot(temp['norm_ts'], temp['value'])
        axs[4].set_xlabel('Čas [s]')
        axs[4].set_ylabel('Teplota [°C]')
        axs[4].set_yticks(np.arange(30, 38, 1))

        tag['value'] = 1
        axs[5].scatter(tag['norm_ts'], tag['value'])
        axs[5].set_xlabel('Čas [s]')
        axs[5].set_ylabel('Značka')
        axs[5].set_yticks(np.arange(0.5, 2, 0.5))

        if fig_location:
            plt.savefig('{}/{}.png'.format(fig_location, file))
        else:
            path = os.path.dirname(os.getcwd())
            path = '{}/data/{}/raw'.format(path, file)
            p = Path(path)
            p.mkdir(exist_ok=True)

            plt.savefig('{}/raw_signals_plot.png'.format(p))

        fig.clear()
        plt.close(fig)

if __name__ == '__main__':
    path = os.path.dirname(os.getcwd())
    path = '{}/plots'.format(path)

    p = Path(path)
    p.mkdir(exist_ok=True)

    plot_data()
