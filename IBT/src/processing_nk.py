# -*- coding: utf-8 -*-
"""
 Project: Bachelor thesis
 Theme: Physiological Data to Analyze and Improve the User Experience
 Author: Daniel Stepanek
 License: GPL 3.0

 VUT FIT Brno 2021

"""

from file_processing import get_all_data
from pathlib import Path, PurePath
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import neurokit2 as nk
import make_stat as ms

plt.rcParams['figure.figsize'] = [15, 5]
plt.rcParams['font.size']= 16

"""
Signals info:

PPG sensor (Blood Volume Pulse (BVP), Hear Rate (HR), IBI): 64hz
EDA sensor (Galvanic skin response (GSR)): 4Hz
IR sensor (Temperature (temp)): 4Hz
Acc sensor: 32Hz
"""

def ibi_miss_ratio(ibi, duration):
    """
        Compute Inter-Beat Interval (E4 data) miss ratio.

        Parameters
        ----------
        ibi : Union [pd.DataFrame]
            Inter-Beat interval (IBI) data.
        duration : int
            Signal duration in seconds.

        Returns
        -------
        int
            IBI miss ratio.
    """

    ibi_dict = ibi.to_dict()
    miss = 0

    ts = list(ibi_dict['timestamp'].values())
    dist = list(ibi_dict['value'].values())
    ibi_len = len(ibi_dict['timestamp'])
    for i in range(ibi_len - 1):
        time_1 = ts[i]
        distance_1 = dist[i]
        time_2 = ts[i + 1]

        if (time_1 + distance_1) < time_2:
            miss += time_2 - time_1 - distance_1

    if duration == 0:
        miss_ratio = 1.0
    else:
        miss_ratio = miss / duration
    print('IBI miss ratio: {}'.format(miss_ratio))

    return miss_ratio


def process_eda(eda, show_fig=False):
    """
        Resample EDA signal from 4 Hz to 64 Hz.
        Compute EDA signal features (more info: https://neurokit2.readthedocs.io/en/latest/functions.html#module-neurokit2.eda).

        Parameters
        ----------
        eda : dict [timestamp : value]
            EDA signal.
        show_fig : bool
            set if plot specific features.

        Returns
        -------
        eda_signals : DataFrame
        eda_info : dict
    """

    eda_signal = nk.signal_resample(eda['value'], sampling_rate=4, desired_sampling_rate=64)
    eda_signals, eda_info = nk.eda_process(eda_signal, sampling_rate=64)

    if show_fig:
        plt.plot(eda_signals['EDA_Phasic'], label='fázická složka')
        plt.plot(eda_signals['EDA_Tonic'], label='tónická složka')
        plt.plot(eda_signals['EDA_Raw'], label='původní')
        plt.xlabel('Vzorek [n]')
        plt.ylabel('EDA [uS]')
        plt.legend()
        plt.show()

    return eda_signals, eda_info


def process_bvp(bvp, show_fig=False):
    """
        Compute BVP signal features (more info: https://neurokit2.readthedocs.io/en/latest/functions.html#module-neurokit2.ppg).
        Compute HRV indices (more info: https://neurokit2.readthedocs.io/en/latest/functions.html#module-neurokit2.hrv)
        Parameters
        ----------
        bvp : dict [timestamp : value]
            EDA signal.

        Returns
        -------
        bvp_signals : DataFrame
        bvp_info : dict
    """

    bvp_signals, bvp_info = nk.ppg_process(bvp['value'], sampling_rate=64)


    # First 5 seconds of the signal.
    # Find peaks
    peaks = bvp_signals['PPG_Peaks'][:320]

    # Compute HRV indices
    time_hrv = nk.hrv_time(peaks, sampling_rate=64, show=show_fig)

    hrv_base = time_hrv
    hrv_base['type'] = 'base'

    # The rest part of the signal.
    # Find peaks
    peaks = bvp_signals['PPG_Peaks'][320:]

    # Compute HRV indices
    phase_hrv = nk.hrv_frequency(peaks, sampling_rate=64, show=show_fig)
    time_hrv = nk.hrv_time(peaks, sampling_rate=64, show=show_fig)
    nonlinear_hrv = nk.hrv_nonlinear(peaks, sampling_rate=64, show=show_fig)

    hrv_indices = pd.concat([phase_hrv, time_hrv, nonlinear_hrv], axis=1)
    hrv_indices['type'] = 'stimul'

    hrv_indices = pd.concat([hrv_indices, hrv_base])

    return bvp_signals, bvp_info, hrv_indices

def find_events(signals, tag, condition_list=None, treshold_keep='below', duration=1, sample_rate=64):
    """
        Create array of events (length: duration * sample_rate) marked by tag signal.

        Parameters
        ----------
        signals : Union [pd.DataFrame]
            BVP and EDA signals.

        tag : Union [pd.DataFrame]
            Tag data from E4. Marked events by participant.

        condition_list : list
            Emotions for each epoch. Length must be the same as tag length.

        treshold_keep : str ['below', 'above']
            Parameter for 'events_find' function.

        duration : int
            Set length of event.

        sample_rate : int
            Sample rate of signals (must be same for all signals).

        Returns
        -------
        dict
            Dict of events (more info: https://neurokit2.readthedocs.io/en/latest/functions.html#module-neurokit2.events).
            {'onset': array(...),
            'duration': array(...),
            'label': array(...)}

    """

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
    """
        Extract Event-Related Features (more info: https://neurokit2.readthedocs.io/en/latest/examples/eventrelated.html)
        First epoch is used as base.

        Parameters
        ----------
        epochs : DataFrame
            Epochs created by function 'epoch_create' (more info: https://neurokit2.readthedocs.io/en/latest/functions.html#module-neurokit2.epochs)
        condition_list : list
            Emotions for each epoch.

        Returns
        -------
        DataFrame
            Dataframe of epochs with extracted features. {'PPG_Rate' : float,
                                                          'EDA_Tonic' : float,
                                                          'EDA_Phasic' : float,
                                                          'Condition' : str}

    """

    epoch_dict = {}

    ppg_baseline = epochs['1']['PPG_Rate'][1:].mean()
    eda_phasic_baseline = epochs['1']['EDA_Phasic'][1:].mean()
    eda_tonic_baseline = epochs['1']['EDA_Tonic'][1:].mean()

    for epoch_index in epochs:
        epoch_dict[epoch_index] = {}
        epoch = epochs[epoch_index]

        if epoch_index == '1':
            epoch_dict[epoch_index]['PPG_Rate'] = ppg_baseline
            epoch_dict[epoch_index]['EDA_Tonic'] = eda_tonic_baseline
            epoch_dict[epoch_index]['EDA_Phasic'] = eda_phasic_baseline
            continue

        #Select data from the epoch (response on stimul).
        ppg_mean = epoch['PPG_Rate'].loc[1:].mean()
        epoch_dict[epoch_index]['PPG_Rate'] = ppg_mean - ppg_baseline

        eda_mean = epoch['EDA_Tonic'].loc[1:].mean()
        epoch_dict[epoch_index]['EDA_Tonic'] = eda_mean - eda_tonic_baseline

        eda_mean = epoch['EDA_Phasic'].loc[1:].mean()
        epoch_dict[epoch_index]['EDA_Phasic'] = eda_mean - eda_phasic_baseline

    df = pd.DataFrame.from_dict(epoch_dict, orient='index')
    if condition_list:
        df['Condition'] = condition_list

    return df

def plot_epochs(folder, epochs, events):
    """
        Plot computed features for each epoch.

        Parameters
        ----------
        folder : str
            Name of actual data folder.
        epochs : DataFrame
            Epochs created by function 'epoch_create' (more info: https://neurokit2.readthedocs.io/en/latest/functions.html#module-neurokit2.epochs)
        events : dict
            Events created by function 'events_find'.

    """

    for i, epoch in enumerate (epochs):
        epoch = epochs[epoch]

        epoch = epoch[['PPG_Raw', 'PPG_Clean', 'PPG_Rate', 'PPG_Peaks',
                       'EDA_Raw', 'EDA_Clean', 'EDA_Phasic', 'EDA_Tonic',
                       'SCR_Onsets', 'SCR_Peaks', 'SCR_Amplitude', 'SCR_RiseTime',
                       'SCR_Recovery']]

        # get title from condition list
        title = events['condition'][i]

        epoch.plot(title=title, legend=True)
    plt.show()

def save_epochs_to_csv(path, epochs):
    """
        Save epochs dataframes as csv to epoch folder.

        Parameters
        ----------
        path : str
            Epochs data path. To this folder is created epochs folder, where csv files will be saved.
        epochs : DataFrame
            Epochs created by function 'epoch_create' (more info: https://neurokit2.readthedocs.io/en/latest/functions.html#module-neurokit2.epochs)

    """

    p = Path('{}/epochs'.format(path))
    p.mkdir(exist_ok=True)

    for i, epoch in enumerate(epochs):
        epoch = epochs[epoch]

        epoch = epoch[['PPG_Raw', 'PPG_Clean', 'PPG_Rate', 'PPG_Peaks',
                       'EDA_Raw', 'EDA_Clean', 'EDA_Phasic', 'EDA_Tonic',
                       'SCR_Onsets', 'SCR_Peaks', 'SCR_Amplitude', 'SCR_RiseTime',
                       'SCR_Recovery', 'Index', 'Condition']]

        emotion = epoch['Condition'].head(1).values[0]
        epoch.to_csv('{}/epochs/{}_{}.csv'.format(path, i, emotion))

def concat_epochs_by_condition(epochs):
    """
        Concatenate all epochs by emotion.

        Parameters
        ----------
        epochs : DataFrame
            Epochs created by function 'epoch_create' (more info: https://neurokit2.readthedocs.io/en/latest/functions.html#module-neurokit2.epochs)

        Returns
        -------
        neutral_df : DataFrame
            Dataframe with data of all neutral epochs.
        emotion_df : DataFrame
            Dataframe with data of all epochs where participant should feel emotion.

    """

    emotion_df = pd.DataFrame()
    neutral_df = pd.DataFrame()

    for i, epoch in enumerate(epochs):
        epoch = epochs[epoch]
        epoch.reset_index(level=0, inplace=True)
        #number of epoch
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


class Processor:
    """
        Main class for data processing.
        Data can be processed for one session (process_session) or for all sessions (process_all).
        If all sessions are processed, statistics will be made.
    """


    def __init__(self, path, show_fig=False, plot_epochs=False):
        """
            Parameters
            ----------
            path : str
                set path of sessions data.

            show_fig : bool
                If set, plot figures.

            plot_epochs : bool
                If set, plot data of all epochs of all sessions (warning: time consuming).

        """

        self.path = path
        self.show_fig = show_fig
        self.plot_epochs = plot_epochs

        self.emotion_gender_dict = {'emotion' : [], 'gender' : []}
        self.erf_all = pd.DataFrame()   #event-related features of all sessions
        self.samples_count = 0
        self.folders_count = 0
        self.ppg_ratio = 0  #ppg overall miss ratio

        #emotion : [count_of_samples, ppg_ratio_sum]
        self.ppg_ratio_dict = {'nuda' : [0, 0],
                               'pozitivni' : [0, 0],
                               'radost' : [0, 0],
                               'strach' : [0, 0],
                               'zmatek' : [0, 0],
                               'znechuceni' : [0, 0]
                              }

    def statistics(self):
        """
            Make and plot statistics for all sessions.
        """

        if self.folders_count == 0:
            print('No data for statistics.')
            return

        self.ppg_ratio = self.ppg_ratio / self.folders_count
        print('----------------------------------------')
        print('PPG Miss Ratio: {}'.format(self.ppg_ratio))
        print('----------------------------------------')
        #ppg miss ratio for each emotion.
        for emotion, stat in self.ppg_ratio_dict.items():
            if stat[0] != 0:
                ratio = stat[1] / stat[0]
                print('{} : {}'.format(emotion, ratio))
            else:
                print('{} : {}'.format(emotion, 'undef'))
        print('----------------------------------------')

        self.erf_all.to_csv('{}/Event_Related_Features.csv'.format(self.path))

        emotion_gender_df = pd.DataFrame.from_dict(self.emotion_gender_dict)
        emotion_gender_df = emotion_gender_df[['emotion', 'gender']]
        emotion_gender_df.to_csv('{}/Emotion_Gender.csv'.format(self.path))

        ms.dataset_stat(self.samples_count, self.folders_count)
        ms.hr_eda_stat(self.path)
        ms.plot_heatmap_emotion_choice(self.path)
        ms.plot_stat(self.path, emotion_gender_df)
        print('statistics done')
        ms.plot_features(self.path, self.erf_all)
        print('features done')

        #warning: time consuming
        if self.plot_epochs:
            ms.plot_signals_for_all_epochs_by_emotion(self.path)
            print('epochs done')


    def process_all(self):
        """
            Process and make statistics for all sessions data.
        """

        for folder, data in get_all_data(path=self.path):
            if not data:
                continue

            print(folder)

            self.folders_count += 1

            erf = self.process_session(folder, data)
            #If something went wrong in session processing.
            if type(erf) != type(pd.DataFrame()):
                print('Cannot process {}.'.format(folder))
                continue

            if self.erf_all.empty:
                self.erf_all = erf.copy()
            else:
                self.erf_all = pd.concat([self.erf_all, erf])

        self.statistics()


    def process_session(self, folder, data):
        """
            Process session data.

            Parameters
            ----------
            folder : str
                Session data folder name.
            data : DataFrame
                Session data.

            Returns
            -------
            DataFrame
                Extracted event-related features for all signals.

        """

        p = Path('{}/{}/epochs'.format(self.path, folder))
        p.mkdir(exist_ok=True)

        name = folder.split('_')
        emotion = name[0]
        gender = name[-1]

        self.emotion_gender_dict['emotion'] += [emotion]
        self.emotion_gender_dict['gender'] += [gender]

        bvp = data['bvp']
        eda = data['gsr']
        tag = data['tag']
        hr = data['hr']
        ibi = data['ibi']

        #epoch count / 2
        count = tag.shape[0] // 2
        if count == 0:
            count = 1

        self.samples_count += count

        condition_list = ['neutral', emotion] * count

        #Remove data before the first tag and after the last tag.
        first_tag = tag['norm_ts'].head(1).values[0]

        tag.loc[:,'norm_ts'] -= first_tag
        bvp.loc[:,'norm_ts'] -= first_tag
        eda.loc[:,'norm_ts'] -= first_tag
        hr.loc[:,'norm_ts'] -= first_tag
        ibi.loc[:,'norm_ts'] -= first_tag

        tag = tag[tag['norm_ts'] >= 0.0]
        bvp = bvp[bvp['norm_ts'] >= 0.0]
        eda = eda[eda['norm_ts'] >= 0.0]
        hr = hr[hr['norm_ts'] >= 0.0]
        ibi = ibi[ibi['norm_ts'] >= 0.0]

        last_tag = tag['norm_ts'].tail(1).values[0]

        tag = tag[tag['norm_ts'] < last_tag]
        bvp = bvp[bvp['norm_ts'] <= last_tag]
        eda = eda[eda['norm_ts'] <= last_tag]
        hr = hr[hr['norm_ts'] <= last_tag]
        ibi = ibi[ibi['norm_ts'] <= last_tag]

        #Compute IBI miss ratio
        duration = tag['timestamp'].tail(1).values[0] - tag['timestamp'].head(1).values[0]
        m_ratio = ibi_miss_ratio(ibi, duration)
        self.ppg_ratio += m_ratio
        self.ppg_ratio_dict[emotion][0] += 1
        self.ppg_ratio_dict[emotion][1] += m_ratio

        #Process the Signals
        try:
            eda_signals, eda_info = process_eda(eda)
            bvp_signals, bvp_info, hrv_indices = process_bvp(bvp)
            hrv_indices['Condition'] = emotion
            hrv_indices.to_csv('{}/{}/hrv.csv'.format(self.path, folder))
        except Exception as e:
            print('Signal processing for {} failed.'.format(folder))
            print('Raised exception: {}. Signal processing handler.'.format(e))
            return None

        signals = pd.concat([bvp_signals, eda_signals], axis=1, join='inner')
        signals = signals.fillna(0)
        signals.to_csv('{}/{}/signals.csv'.format(self.path, folder))

        #reset index to start by 0.
        bvp_signals.reset_index(inplace=True)

        #plot HR from E4 with HR computed by NeuroKit2.
        if self.show_fig and m_ratio < 0.01:
            plt.plot(hr['norm_ts']+5, hr['value'], label='Empatica E4')
            plt.plot(bvp_signals['index'][::64]/64, bvp_signals['PPG_Rate'][::64], label='NeuroKit2')
            plt.xlabel('Čas [s]')
            plt.ylabel('Srdeční tep [bpm]')
            plt.legend()
            plt.show()

        try:
            events = find_events(signals, tag, condition_list=condition_list)
            epochs = nk.epochs_create(signals, events, sampling_rate=64, epochs_start=0)
        except Exception as e:
            print('Signal processing for {} failed.'.format(folder))
            print('Raised exception: {}. Epochs creating handler.'.format(e))
            return None

        neutral_df, emotion_df = concat_epochs_by_condition(epochs)
        neutral_df.to_csv('{}/{}/epochs/neutral_all.csv'.format(self.path, folder))
        emotion_df.to_csv('{}/{}/epochs/emotion_all.csv'.format(self.path, folder))

        save_epochs_to_csv('{}/{}'.format(self.path, folder), epochs)

        if self.show_fig:
            plot_epochs(folder, epochs, events)

        #Extract Event Related Features
        erf = extract_ERF(epochs, condition_list=condition_list)
        erf['Gender'] = gender
        erf.to_csv('{}/{}/features.csv'.format(self.path, folder))


        return erf


if __name__ == '__main__':
    path = os.path.dirname(os.getcwd())
    path = '{}/data'.format(path)
    processor = Processor(path=path)
    processor.process_all()
