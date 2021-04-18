# -*- coding: utf-8 -*-
"""

@author: Daniel Stepanek
"""

"""
PPG sensor (Blood Volume Pulse (BVP), Hear Rate (HR), IBI): 64hz
EDA sensor (Galvanic skin response (GSR)): 4Hz
IR sensor (Temperature (temp)): 4Hz
Acc sensor: 32Hz
"""


from file_processing import get_data
from matplotlib.ticker import MaxNLocator

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import neurokit2 as nk


plt.rcParams['figure.figsize'] = [15, 5]
plt.rcParams['font.size']= 14

def process_eda(eda):
    eda_signal = nk.signal_resample(eda['value'], sampling_rate=4, desired_sampling_rate=64)
    eda_signals, eda_info = nk.eda_process(eda_signal, sampling_rate=64)
    
    return eda_signals, eda_info


def process_bvp(bvp):
    bvp_signals, bvp_info = nk.ppg_process(bvp['value'], sampling_rate=64)

    return bvp_signals, bvp_info

def find_events(signals, tag, condition_list=None, treshold_keep='below', duration=1, sample_rate=64):
     if tag.shape[0] != 0:
        tag_signal = np.ones(signals.shape[0])

        #For each marked event set value 0 for
        #(duration * sample_rate) data points.
        events_time = list(tag['norm_ts'])
        for t in events_time:
            end_t = int(t + duration) * sample_rate
            t = int(t * sample_rate)
            tag_signal[t:end_t] = 0

        events = nk.events_find(event_channel=tag_signal,
                                threshold_keep=treshold_keep,
                                event_conditions=condition_list)
        return events

def extract_ERF(epochs, condition_list=None):
    epoch_dict = {}

    for epoch_index in epochs:
        epoch_dict[epoch_index] = {}

        epoch = epochs[epoch_index]
        
        #Select data from the end of the epoch (after response on stimul).
        ppg_baseline = epoch['PPG_Rate'].loc[1:2].mean()
        # Mean heart rate in the 0-4 seconds
        ppg_mean = epoch['PPG_Rate'].loc[2:].mean()

        epoch_dict[epoch_index]['PPG_Rate'] = ppg_mean - ppg_baseline

        scr_max = epoch['SCR_Amplitude'].loc[1:].max()
        if np.isnan(scr_max):
            scr_max = 0

        epoch_dict[epoch_index]['SCR_Magnitude'] = scr_max

    df = pd.DataFrame.from_dict(epoch_dict, orient='index')
    if condition_list:
        df['Condition'] = condition_list

    return df

def plot_epochs(folder, epochs, events):
    for i, epoch in enumerate (epochs):
        epoch = epochs[epoch]

        epoch = epoch[['PPG_Raw', 'PPG_Clean', 'PPG_Rate', 'PPG_Peaks',
                       'EDA_Raw', 'EDA_Clean', 'EDA_Phasic', 'EDA_Tonic',
                       'SCR_Onsets', 'SCR_Peaks', 'SCR_Amplitude', 'SCR_RiseTime',
                       'SCR_Recovery']]

        title = events['condition'][i] # get title from condition list

        epoch.plot(title=title, legend=True)  # Plot scaled signals
    plt.show()

def save_epochs_to_csv(path, epochs):
    
    for i, epoch in enumerate(epochs):
        epoch = epochs[epoch]
        
        epoch = epoch[['PPG_Raw', 'PPG_Clean', 'PPG_Rate', 'PPG_Peaks',
                       'EDA_Raw', 'EDA_Clean', 'EDA_Phasic', 'EDA_Tonic',
                       'SCR_Onsets', 'SCR_Peaks', 'SCR_Amplitude', 'SCR_RiseTime',
                       'SCR_Recovery', 'Index', 'Condition']]
        
        emotion = epoch['Condition'].head(1).values[0]
        epoch.to_csv('{}\\{}_{}.csv'.format(path, i, emotion))


def make_stat(folder_name_df, erf_df, path):
    
    plt.figure(figsize=(9,5))
    
    f = sns.histplot(data=folder_name_df,
                     x='emotion', binwidth=5)
    f.set_xlabel('Emoce')
    f.set_ylabel('Počet')
    f.yaxis.set_major_locator(MaxNLocator(integer=True))
    f.set_xticklabels(['Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])
    
    handles, _ = f.get_legend_handles_labels()
    f.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}\\hist.png'.format(path))
    plt.show()
    
    
    g = sns.countplot(data=folder_name_df,
                      x='emotion', hue="gender") 
    g.set_xlabel('Emoce')
    g.set_ylabel('Počet')
    g.yaxis.set_major_locator(MaxNLocator(integer=True))
    g.set_xticklabels(['Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])
    
    handles, _ = g.get_legend_handles_labels()
    g.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}\\emotion_count.png'.format(path))
    plt.show()
    
    
    h = sns.boxplot(x='Condition', y='PPG_Rate', hue='Gender', data=erf_df)
    h.set_xlabel('Emoce')
    h.set_ylabel('Srdeční tep')
    h.yaxis.set_major_locator(MaxNLocator(integer=True))
    h.set_xticklabels(['Neutrální', 'Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])

    handles, _ = h.get_legend_handles_labels()
    h.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}\\heart_rate.png'.format(path))
    plt.show()

    
    
    
    
def process_data(path, show_fig=False):
    
    folder_name_dict = {'emotion' : [], 'gender' : []}
    
    erf_df = pd.DataFrame()
    
    for folder, data in get_data(path=path):
        print(folder)
        bvp = data['bvp']
        eda = data['gsr']
        tag = data['tag']

        name = folder.split('_')
        emotion = name[0]
        gender = name[-1]
        
        folder_name_dict['emotion'] += [emotion]
        folder_name_dict['gender'] += [gender]
        
        count = tag.shape[0] // 2
        if count == 0:
            count = 1

        condition_list = ['neutral', emotion] * count

        #Remove data before the first tag and after the last tag.
        first_tag = tag['norm_ts'].head(1).values[0]

        tag.loc[:,'norm_ts'] -= first_tag
        bvp.loc[:,'norm_ts'] -= first_tag
        eda.loc[:,'norm_ts'] -= first_tag

        tag = tag[tag['norm_ts'] >= 0.0]
        bvp = bvp[bvp['norm_ts'] >= 0.0]
        eda = eda[eda['norm_ts'] >= 0.0]

        last_tag = tag['norm_ts'].tail(1).values[0]

        tag = tag[tag['norm_ts'] < last_tag]
        bvp = bvp[bvp['norm_ts'] <= last_tag]
        eda = eda[eda['norm_ts'] <= last_tag]

        #Process the Signals
        eda_signals, eda_info = process_eda(eda)
        bvp_signals, bvp_info = process_bvp(bvp)
        
        cleaned = eda_signals["EDA_Clean"]
        features = [eda_info["SCR_Onsets"], eda_info["SCR_Peaks"], eda_info["SCR_Recovery"]]
        
        
        signals = pd.concat([bvp_signals, eda_signals], axis=1, join='inner')
        signals = signals.fillna(0)
        signals.to_csv('{}\\{}\\signals.csv'.format(path, folder))

        events = find_events(signals, tag, condition_list=condition_list)

        epochs = nk.epochs_create(signals, events, sampling_rate=64, epochs_start=-1, epochs_end=6)

        save_epochs_to_csv('{}\\{}'.format(path, folder), epochs)

       # if show_fig:
       #     plot_epochs(folder, epochs, events)

        #Extract Event Related Features
        erf = extract_ERF(epochs, condition_list=condition_list)
        erf.to_csv('{}\\{}\\features.csv'.format(path, folder))

        erf['Gender'] = gender
        if erf_df.empty:
            erf_df = erf.copy()
        else:
            erf_df = pd.concat([erf_df, erf])
        
        if show_fig:
            sns.boxplot(x='Condition', y='PPG_Rate', data=erf)
            plt.show()

            sns.boxplot(x='Condition', y='SCR_Magnitude', data=erf)
            plt.show()

    erf_df.to_csv('{}\\Event_Related_Features.csv'.format(path))

    folder_name_df = pd.DataFrame.from_dict(folder_name_dict)
    make_stat(folder_name_df, erf_df, path)
    
    
if __name__ == '__main__':
    path = '.\\data'
    process_data(path, False)
