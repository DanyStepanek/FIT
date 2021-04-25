# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:42:00 2021

@author: Daniel Stepanek
"""




from file_processing import get_data

import sys
import numpy as np
import pandas as pd
import pyphysio as ph
import matplotlib.pyplot as plt



"""
PPG sensor (Blood Volume Pulse (BVP), Hear Rate (HR), IBI): 64hz
EDA sensor (Galvanic skin response (GSR)): 4Hz
IR sensor (Temperature (temp)): 4Hz
Acc sensor: 32Hz
"""

def plot_signals(bvp_s, bvp_label, gsr_s, gsr_label,
                 hr_s, hr_label, ibi_s, ibi_label, temp_s, temp_label):
    
    ax1 = plt.subplot(211)
    bvp_s.plot('.-')

    plt.subplot(212, sharex = ax1)
    bvp_label.plot('.-')
        
    plt.show()
        
    ax1 = plt.subplot(211)
    gsr_s.plot('.-')

    plt.subplot(212, sharex = ax1)
    gsr_label.plot('.-')
        
    plt.show()
        
    ax1 = plt.subplot(211)
    hr_s.plot('.-')

    plt.subplot(212, sharex = ax1)
    hr_label.plot('.-')
        
    plt.show()
    
    ax1 = plt.subplot(211)
    ibi_s.plot('.-')
        
    plt.subplot(212, sharex = ax1)
    ibi_label.plot('.-')
        
    plt.show()
        
    ax1 = plt.subplot(211)
    temp_s.plot('.-')
        
    plt.subplot(212, sharex = ax1)
    temp_label.plot('.-')
        
    plt.show()

def get_hrv_indicators(path, file, ibi_s, ibi_label):
    """
    # define a list of indicators we want to compute
    hrv_indicators = [ph.Mean(name='RRmean'), ph.StDev(name='RRstd'), ph.RMSSD(name='rmsSD')]
            
    #fixed length windowing
    fixed_length = ph.FixedSegments(step = 5, width = 10, labels = ibi_label)
    indicators, col_names = ph.fmap(fixed_length, hrv_indicators, ibi_s)
    #print(indicators.shape)
    #  print(f'indicator: {indicators}, col:{col_names}')
    label_w = indicators[:, np.where(col_names == 'label')[0]]
        
    rrmean_w = indicators[:, np.where(col_names == 'RRmean')[0]]
        
    rrmean_calm = rrmean_w[np.where(label_w==0)[0]].ravel()
    rrmean_impulse = rrmean_w[np.where(label_w==1)[0]].ravel()
     
        
    plt.boxplot([rrmean_calm, rrmean_impulse],
                    labels=['calm', 'impulse'])
        
    """
        
    #fixed length windowing
    fixed_length = ph.FixedSegments(step = 5, width = 10, labels = ibi_label)

    HRV_FD = ph.preset_hrv_fd()
    FD_HRV_ind, col_names = ph.fmap(fixed_length, ph.preset_hrv_fd(), ibi_s.resample(4))
        
    FD_HRV_df = pd.DataFrame(FD_HRV_ind, columns=col_names)
        
    FD_HRV_df.to_csv(r'{}/{}/hrv_indicators.csv'.format(path, file), 
                                            index=False, header=True)
            
            
    
    
    
def data_to_signal(data):
    bvp = data['bvp']
    gsr = data['gsr']
    hr = data['hr']
    ibi = data['ibi']
    temp = data['temp']
        
    hr_start_t = list(hr['norm_ts'])[0]
    ibi_start_t = list(ibi['norm_ts'])[0]
    bvp_start_t = list(bvp['norm_ts'])[0]
    gsr_start_t = list(gsr['norm_ts'])[0]
    temp_start_t = list(temp['norm_ts'])[0]
        
    # create the Evenly signal      
    hr_s = ph.EvenlySignal(values = hr['value'], sampling_freq = 1, signal_type  = 'hr', start_time = hr_start_t)
    ibi_s = ph.EvenlySignal(values = ibi['value'], sampling_freq = 1, signal_type  = 'ibi', start_time = ibi_start_t)
    bvp_s = ph.EvenlySignal(values = bvp['value'], sampling_freq = 64, signal_type = 'bvp', start_time = bvp_start_t)
    gsr_s = ph.EvenlySignal(values = gsr['value'], sampling_freq = 4, signal_type = 'gsr', start_time = gsr_start_t)
    temp_s = ph.EvenlySignal(values = gsr['value'], sampling_freq = 4, signal_type = 'temp', start_time = temp_start_t)

    return hr_s, ibi_s, bvp_s, gsr_s, temp_s       

def process_data(path):
    for file, data in get_data():
        print(file)
            
        hr_s, ibi_s, bvp_s, gsr_s, temp_s = data_to_signal(data)
        tag = data['tag']
        
        end_time = list(data['bvp']['norm_ts'])[-1]
        
        #creating array for labeling events
        bvp_label = np.zeros(int(end_time))
        gsr_label = np.zeros(int(end_time))
        hr_label = np.zeros(int(end_time))
        ibi_label = np.zeros(int(end_time))
        temp_label = np.zeros(int(end_time))
        
        #for each marked event set value 1 for 10ms
        event_time = list(tag['norm_ts'])
        for t in event_time:
            t = int(t)
            
            bvp_label[t:t+10] = 1
            gsr_label[t:t+20] = 1
            hr_label[t:t+10] = 1
            ibi_label[t:t+10] = 1
            temp_label[t:t+20] = 1
            
        bvp_label = ph.EvenlySignal(bvp_label, sampling_freq=1, signal_type='bvp_label')
        gsr_label = ph.EvenlySignal(gsr_label, sampling_freq=1, signal_type='gsr_label')
        hr_label = ph.EvenlySignal(hr_label, sampling_freq=1, signal_type='hr_label')
        ibi_label = ph.EvenlySignal(ibi_label, sampling_freq=1, signal_type='ibi_label')
        temp_label = ph.EvenlySignal(temp_label, sampling_freq=1, signal_type='temp_label')
        
        
        plot_signals(bvp_s, bvp_label, gsr_s, gsr_label,
                     hr_s, hr_label, ibi_s, ibi_label, temp_s, temp_label)
          
        
        get_hrv_indicators(path, file, ibi_s, ibi_label)
        
        gsr_s = gsr_s.resample(fout=8, kind='cubic')
        gsr_filt = ph.IIRFilter(fp=0.8, fs=1.1, ftype='ellip')(gsr_s)
        
        gsr_s = gsr_filt
        driver = ph.DriverEstim()(gsr_s)
        
        # compute the phasic component
        phasic, tonic, _ = ph.PhasicEstim(delta=0.02)(driver)

        # check results so far
        plt.figure()
        ax1 = plt.subplot(211)
        gsr_s.plot()
        gsr_label.plot()

        plt.subplot(212, sharex = ax1)
        driver.plot()
        phasic.plot()
        plt.grid()
        plt.show()
        
        #fixed length windowing
        fixed_length = ph.FixedSegments(step = 5, width = 20, labels = gsr_label)

        # we use the preset indicators for the phasic signal.
        # We need to define the minimum amplitude of the peaks that will be considered
        PHA_ind, col_names = ph.fmap(fixed_length, ph.preset_phasic(delta=0.02), phasic)
        
        if PHA_ind.shape[0] == 0:
            continue
        
        ## extract column with the labels for each window
        label_w = PHA_ind[:, np.where(col_names == 'label')[0]]

        ## extract column with the PksMean values
        ## computed from each window
        pksmean_w = PHA_ind[:, np.where(col_names == 'pha_PeaksMean')[0]]

        pksmean_calm = pksmean_w[np.where(label_w==0)[0]]
        pksmean_impulse = pksmean_w[np.where(label_w==1)[0]]

        ## create a box and whisker plot 
        ## to compate the distibution of the RRmean indicator
        plt.figure()
        print(pksmean_calm.shape)
        #plt.boxplot([pksmean_calm, pksmean_impulse], 
        #            labels=['calm', 'impulse'])
        #plt.show()
        
        
        
if __name__ == '__main__':
    path = 'C:\\Users\\dandi\\Dropbox\\skola FIT\\bakalarka\\client_E4\\data'
    process_data(path)
    
    
    