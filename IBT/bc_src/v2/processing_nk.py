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
from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import neurokit2 as nk
import make_stat as ms

plt.rcParams['figure.figsize'] = [15, 5]
plt.rcParams['font.size']= 16

def process_eda(eda):
    eda_signal = nk.signal_resample(eda['value'], sampling_rate=4, desired_sampling_rate=64)
    eda_signals, eda_info = nk.eda_process(eda_signal, sampling_rate=64)

#    plt.plot(eda_signals[['EDA_Raw', 'EDA_Clean']][100:300])
#    plt.legend(eda_signals.columns)
#    plt.show()

    return eda_signals, eda_info


def process_bvp(bvp):
    bvp_signals, bvp_info = nk.ppg_process(bvp['value'], sampling_rate=64)

    # Compute HRV indices
    hrv_indices = nk.hrv(bvp_signals['PPG_Peaks'], sampling_rate=64, show=False)

#    plt.plot(bvp_signals[['PPG_Raw', 'PPG_Clean']][100:300])
#    plt.legend(bvp_signals.columns)
#    plt.show()

    return bvp_signals, bvp_info, hrv_indices

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

        #Select data from the epoch (response on stimul).
        ppg_baseline = epoch['PPG_Rate'].loc[1:2].mean()
        ppg_mean = epoch['PPG_Rate'].loc[2:].mean()
        epoch_dict[epoch_index]['PPG_Rate'] = ppg_mean - ppg_baseline

        eda_baseline = epoch['EDA_Tonic'].loc[1:2].mean()
        eda_mean = epoch['EDA_Tonic'].loc[2:].mean()
        epoch_dict[epoch_index]['EDA_Tonic'] = eda_mean - eda_baseline

        eda_baseline = epoch['EDA_Phasic'].loc[1:2].mean()
        eda_mean = epoch['EDA_Phasic'].loc[2:].mean()
        epoch_dict[epoch_index]['EDA_Phasic'] = eda_mean - eda_baseline

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
    p = Path('{}\\epochs'.format(path))
    p.mkdir(exist_ok=True)

    for i, epoch in enumerate(epochs):
        epoch = epochs[epoch]

        epoch = epoch[['PPG_Raw', 'PPG_Clean', 'PPG_Rate', 'PPG_Peaks',
                       'EDA_Raw', 'EDA_Clean', 'EDA_Phasic', 'EDA_Tonic',
                       'SCR_Onsets', 'SCR_Peaks', 'SCR_Amplitude', 'SCR_RiseTime',
                       'SCR_Recovery', 'Index', 'Condition']]

        emotion = epoch['Condition'].head(1).values[0]
        epoch.to_csv('{}\\epochs\\{}_{}.csv'.format(path, i, emotion))

def concat_epochs_by_condition(epochs):
    emotion_df = pd.DataFrame()
    neutral_df = pd.DataFrame()

    for i, epoch in enumerate(epochs):
        epoch = epochs[epoch]
        epoch.reset_index(level=0, inplace=True)

        epoch['id'] = i

        if i % 2:
            if emotion_df.empty:
                emotion_df = epoch.copy()
            else:
                emotion_df = pd.concat([emotion_df, epoch])
        else:
            if neutral_df.empty:
                neutral_df = epoch.copy()
            else:
                neutral_df = pd.concat([neutral_df, epoch])

    return neutral_df, emotion_df


def process_data(path, show_fig=False, plot_epochs=False):

    emotion_gender_dict = {'emotion' : [], 'gender' : []}
    erf_df = pd.DataFrame()

    samples_count = 0
    folders_count = 0

    for folder, data in get_data(path=path):
        print(folder)

        folders_count += 1

        p = Path('{}\\{}\\epochs'.format(path, folder))
        p.mkdir(exist_ok=True)

        bvp = data['bvp']
        eda = data['gsr']
        tag = data['tag']

        name = folder.split('_')
        emotion = name[0]
        gender = name[-1]

        emotion_gender_dict['emotion'] += [emotion]
        emotion_gender_dict['gender'] += [gender]

        #epoch count / 2
        count = tag.shape[0] // 2
        if count == 0:
            count = 1

        samples_count += count

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
        try:
            eda_signals, eda_info = process_eda(eda)
            bvp_signals, bvp_info, hrv = process_bvp(bvp)
            hrv.to_csv('{}\\{}\\hrv.csv'.format(path, folder))
        except Exception as e:
            print(e)
            continue

        signals = pd.concat([bvp_signals, eda_signals], axis=1, join='inner')
        signals = signals.fillna(0)
        signals.to_csv('{}\\{}\\signals.csv'.format(path, folder))

        try:
            events = find_events(signals, tag, condition_list=condition_list)
            epochs = nk.epochs_create(signals, events, sampling_rate=64, epochs_start=0, epochs_end=7)
        except Exception as e:
            print(e)
            continue

        neutral_df, emotion_df = concat_epochs_by_condition(epochs)
        neutral_df.to_csv('{}\\{}\\epochs\\neutral_all.csv'.format(path, folder))
        emotion_df.to_csv('{}\\{}\\epochs\\emotion_all.csv'.format(path, folder))

        save_epochs_to_csv('{}\\{}'.format(path, folder), epochs)

        if show_fig:
            plot_epochs(folder, epochs, events)

        #Extract Event Related Features
        erf = extract_ERF(epochs, condition_list=condition_list)
        erf.to_csv('{}\\{}\\features.csv'.format(path, folder))

        erf['Gender'] = gender
        if erf_df.empty:
            erf_df = erf.copy()
        else:
            erf_df = pd.concat([erf_df, erf])

        fig, axs = plt.subplots(nrows=2, sharex=True, constrained_layout=True)
        ax0 = sns.boxplot(ax=axs[0], x='Condition', y='PPG_Rate', data=erf)
        ax0.set_ylabel('Srdeční tep [bpm]')

        ax1 = sns.boxplot(ax=axs[1], x='Condition', y='EDA_Phasic', data=erf)
        ax1.set_ylabel('Fázická složka [uS]')

        plt.savefig('{}\\{}\\rate_phasic.png'.format(path, folder))

        if show_fig:
            plt.show()

        fig.clear()
        plt.close(fig)

    erf_df.to_csv('{}\\Event_Related_Features.csv'.format(path))

    emotion_gender_df = pd.DataFrame.from_dict(emotion_gender_dict)
    emotion_gender_df.to_csv('{}\\Emotion_Gender.csv'.format(path))

    #statistics
    ms.dataset_stat(samples_count, folders_count)
    ms.heart_rate_stat(path)

    ms.plot_stat(path, emotion_gender_df)
    print('statistics done')
    ms.plot_features(path, erf_df)
    print('features done')

    if plot_epochs:
        ms.plot_signals_for_all_epochs_by_emotion(path)
        print('epochs done')


if __name__ == '__main__':
    path = '.\\data'
    process_data(path, False)
