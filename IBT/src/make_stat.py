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
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from file_processing import get_data
from scipy.stats import f_oneway

plt.rcParams['figure.figsize'] = [10, 6]
plt.rcParams['font.size']= 18

def plot_stat(path, emotion_gender_df, show_fig=False):
    """
        Print and plot general statistics about dataset.

        Histogram plot, mean and std value of count of sessions divided by emotion.

        Statistic F-oneway test where gender dependence is tested.

        Histogram of count of data divided by gender and emotion.

        Parameters
        ----------

        path : str
            Path where data are stored.

        emotion_gender_df : DataFrame
            Dataframe with two columns [emotion, gender] for all sessions.

        show_fig : bool
            If set, show plots.

    """

    e_g_grouped = emotion_gender_df.groupby('emotion')
    e_g_count = e_g_grouped.count()
    e_g_mean = e_g_count.mean()
    e_g_std = e_g_count.std()

    print('\nStatistic')
    print('----------------------------------------')
    print('Samples Mean: \n{}'.format(e_g_mean))
    print('Samples Std: \n{}'.format(e_g_std))
    print('----------------------------------------')

    #F-oneway statistic test
    e_g = emotion_gender_df.copy()
    e_g['count'] = 1
    e_g_grouped = e_g.groupby(['emotion', 'gender'])
    e_g_count = e_g_grouped.count().reset_index()

    nuda = e_g_count['count'].loc[e_g_count['emotion'] == 'nuda']
    pozitivni = e_g_count['count'].loc[e_g_count['emotion'] == 'pozitivni']
    radost = e_g_count['count'].loc[e_g_count['emotion'] == 'radost']
    strach = e_g_count['count'].loc[e_g_count['emotion'] == 'strach']
    zmatek = e_g_count['count'].loc[e_g_count['emotion'] == 'zmatek']
    znechuceni = e_g_count['count'].loc[e_g_count['emotion'] == 'znechuceni']

    F, p_value = f_oneway(nuda, pozitivni, radost, strach, zmatek, znechuceni)
    print('F: {}'.format(F))
    print('p-value: {}'.format(p_value))
    print('----------------------------------------')

    #Histogram plot of count of sessions divided by emotion.
    f = sns.histplot(data=emotion_gender_df,
                     x='emotion', shrink=.9, discrete=True)
    f.set_xlabel('Emoce')
    f.set_ylabel('Počet')
    f.yaxis.set_major_locator(MaxNLocator(integer=True))
    f.set_xticklabels(['Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])

    handles, _ = f.get_legend_handles_labels()
    f.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.ylim(0, 20)
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(rotation=0, fontsize=15)
    plt.savefig('{}/hist.png'.format(path))

    if show_fig:
        plt.show()

    f.clear()
    plt.cla()
    plt.clf()

    #Histogram of count of data divided by gender and emotion.
    g = sns.countplot(data=emotion_gender_df,
                      x='emotion', hue="gender")
    g.set_xlabel('Emoce')
    g.set_ylabel('Počet')
    g.yaxis.set_major_locator(MaxNLocator(integer=True))
    g.set_xticklabels(['Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])

    handles, _ = g.get_legend_handles_labels()
    g.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.ylim(0, 12)
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(rotation=0, fontsize=15)
    plt.savefig('{}/emotion_count.png'.format(path))

    if show_fig:
        plt.show()

    g.clear()
    plt.cla()
    plt.clf()


def plot_features(path, erf_df, show_fig=False):
    """
        Plot boxplot for heart rate, EDA phasic and tonic component.

        Parameters
        ----------

        path : str
            Path where data are stored.

        erf_df : DataFrame
            Dataframe containing all event-related features for all sessions.

        show_fig : bool
            If set, show plots.

    """


    f = sns.boxplot(x='Condition', y='PPG_Rate', hue='Gender', data=erf_df)
    f.set_xlabel('Emoce')
    f.set_ylabel('Rozdíl středních hodnot tepu [bpm]')
    f.yaxis.set_major_locator(MaxNLocator(integer=True))
    f.set_xticklabels(['Neutrální', 'Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])

    handles, _ = f.get_legend_handles_labels()
    f.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}/heart_rate.png'.format(path))

    if show_fig:
        plt.show()

    f.clear()
    plt.cla()
    plt.clf()


    g = sns.boxplot(x='Condition', y='EDA_Tonic', hue='Gender', data=erf_df)
    g.set_xlabel('Emoce')
    g.set_ylabel('EDA tónická složka [uS]')
    g.yaxis.set_major_locator(MaxNLocator(integer=True))
    g.set_xticklabels(['Neutrální', 'Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])

    handles, _ = g.get_legend_handles_labels()
    g.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}/eda_tonic.png'.format(path))

    if show_fig:
        plt.show()

    g.clear()
    plt.cla()
    plt.clf()


    h = sns.boxplot(x='Condition', y='EDA_Phasic', hue='Gender', data=erf_df)
    h.set_xlabel('Emoce')
    h.set_ylabel('EDA fázická složka [uS]')
    h.yaxis.set_major_locator(MaxNLocator(integer=True))
    h.set_xticklabels(['Neutrální', 'Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])

    handles, _ = h.get_legend_handles_labels()
    h.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}/eda_phasic.png'.format(path))

    if show_fig:
        plt.show()

    h.clear()
    plt.cla()
    plt.clf()

def plot_ppg(path, folder, neutral_ppg, emotion_ppg):
    """
        Plot heart rate for each session.

        Parameters
        ----------

        path : str
            Path where data are stored.

        folder : str
            Folder name where plot will be stored.

        neutral_ppg : DataFrame
            Dataframe containing data for all neutral epochs of session.

        emotion_ppg : DataFrame
            Dataframe containing data for all emotion epochs of session.

    """

    fig, axs = plt.subplots(nrows=1, ncols=2, sharey=True, constrained_layout=True)
    emotion = folder.split('_')[0]
    fig.suptitle('neutrální - {}'.format(emotion))

    ax0 = sns.lineplot(ax=axs[0], x='index1', y='PPG_Rate', hue='id', data=neutral_ppg)
    ax0.set_xlabel('Vzorek [n]')
    ax0.set_ylabel('Srdeční tep [bpm]')

    ax1 = sns.lineplot(ax=axs[1], x='index1', y='PPG_Rate', hue='id', data=emotion_ppg)
    ax1.set_xlabel('Vzorek [n]')
    ax1.set_ylabel('Srdeční tep [bpm]')

    plt.savefig('{}/{}/heart_rate_compilation.png'.format(path, folder))

    fig.clear()
    plt.close(fig)

def plot_eda(path, folder, neutral_eda, emotion_eda):
    """
        Plot phasic and tonic component of EDA for each session.

        Parameters
        ----------

        path : str
            Path where data are stored.

        folder : str
            Folder name where plot will be stored.

        neutral_ppg : DataFrame
            Dataframe containing data for all neutral epochs of session.

        emotion_ppg : DataFrame
            Dataframe containing data for all emotion epochs of session.

    """

    fig, axs = plt.subplots(nrows=2, ncols=2, constrained_layout=True)
    emotion = folder.split('_')[0]
    #fig.suptitle('neutrální - {}'.format(emotion))

    ax0 = sns.lineplot(ax=axs[0][0], x='index1', y='EDA_Phasic', hue='id', data=neutral_eda)
    ax0.set_xlabel('Vzorek [n]')
    ax0.set_ylabel('Fázická složka [uS]')

    ax1 = sns.lineplot(ax=axs[0][1], x='index1', y='EDA_Phasic', hue='id', data=emotion_eda)
    ax1.set_xlabel('Vzorek [n]')
    ax1.set_ylabel('Fázická složka [uS]')

    ax2 = sns.lineplot(ax=axs[1][0], x='index1', y='EDA_Tonic', hue='id', data=neutral_eda)
    ax2.set_xlabel('Vzorek [n]')
    ax2.set_ylabel('Tónická složka [uS]')

    ax3 = sns.lineplot(ax=axs[1][1], x='index1', y='EDA_Tonic', hue='id', data=emotion_eda)
    ax3.set_xlabel('Vzorek [n]')
    ax3.set_ylabel('Tónická složka [uS]')

    plt.savefig('{}/{}/eda_compilation.png'.format(path, folder))

    fig.clear()
    plt.close(fig)

def plot_signals_for_all_epochs_by_emotion(path):
    """
        Plot signals features for all epochs.

        Parameters
        ----------

        path : str
            Path where data are stored.

    """

    for folder, neutral_df, emotion_df in load_data(path):
        neutral_df['index1'] = neutral_df.index % 384
        emotion_df['index1'] = emotion_df.index % 384

        ppg_cols = ['PPG_Clean', 'PPG_Rate', 'id', 'index1']
        eda_cols =  ['EDA_Tonic', 'EDA_Phasic', 'EDA_Clean', 'id', 'index1']

        neutral_ppg = neutral_df[ppg_cols]
        neutral_eda = neutral_df[eda_cols]
        emotion_ppg = emotion_df[ppg_cols]
        emotion_eda = emotion_df[eda_cols]

        plot_ppg(path, folder, neutral_ppg, emotion_ppg)
        plot_eda(path, folder, neutral_eda, emotion_eda)

def load_data(path):
    """
        Load neutral and emotion dataframe for each session.
        Parameters
        ----------

        path : str
            Path where data are stored.

        Returns
        -------
        Iterator : folder name, neutral dataframe, emotion dataframe

    """

    folders = os.listdir(path)

    for folder in folders:
        folder_path = '{}/{}'.format(path, folder)

        if os.path.isdir(folder_path):
            neutral_df = pd.read_csv('{}/{}/epochs/neutral_all.csv'.format(path, folder))
            emotion_df = pd.read_csv('{}/{}/epochs/emotion_all.csv'.format(path, folder))
            yield folder, neutral_df, emotion_df

def dataset_stat(samples_count=0, folders_count=0):
    """
        Print basic dataset informations (samples count, folders count).

        Parameters
        ----------

        samples_count : int
            Count of samples of all sessions.

        folders_count : int
            Count of all data folders with session data.

    """

    print('\nDataset Statistic')
    print('----------------------------------------')
    print('Samples count: {}'.format(samples_count))
    print('Folders count: {}'.format(folders_count))
    print('----------------------------------------')


def get_mean_hrv_indices(path):
    """
        Get Heart Rate Variability data for all sessions and merge them into one
        dataframe. Dataframe is stored as 'hrv_info.csv'

        Parameters
        ----------

        path : str
            Path where data are stored.

    """


    hrv_dict = {'nuda' : pd.DataFrame(),
                'pozitivni' : pd.DataFrame(),
                'radost' : pd.DataFrame(),
                'strach' : pd.DataFrame(),
                'zmatek' : pd.DataFrame(),
                'znechuceni' : pd.DataFrame(),
                }

    for folder, _, _ in load_data(path):
        emotion = folder.split('_')[0]
        hrv = pd.read_csv('{}/{}/hrv.csv'.format(path, folder))
        if hrv_dict[emotion].empty:
            hrv_dict[emotion] = hrv.copy()
        else:
            hrv_dict[emotion] = hrv_dict[emotion].append(hrv)

    for k, v in hrv_dict.items():
        v.describe().to_csv('{}/{}_hrv_info.csv'.format(path, k))



def plot_heatmap_emotion_choice(path):
    """
        Plot heatmap shows which presentation evokes which emotion.

        Parameters
        ----------

        path : str
            Path where data are stored.

    """


    df = pd.read_csv('{}/emotion_to_presentation.csv'.format(path))
    df = df[df.columns[1:]]
    df = df.fillna(0).astype(int)

    value_c_df = df.apply(pd.value_counts)
    value_c_df = value_c_df.fillna(0).astype(int)
    value_c_df = value_c_df.iloc[1:]

    F, p_value = f_oneway(value_c_df['1'],
                          value_c_df['2'],
                          value_c_df['3'],
                          value_c_df['4'],
                          value_c_df['5'],
                          value_c_df['6'])


    value_c_df = value_c_df.rename(columns={'1' : 'nuda',
                                            '2' : 'pozitivní',
                                            '3' : 'radost',
                                            '4' : 'strach',
                                            '5' : 'zmatek',
                                            '6' : 'znechucení'})

    print('\nEmotion to presentation heatmap')
    print('----------------------------------------')
    print(value_c_df)
    print('----------------------------------------')

    cmap = 'gray_r'
    f = sns.heatmap(data=value_c_df, xticklabels=True, yticklabels=True,
                    cmap=cmap, cbar_kws={'label': 'Počet zvolení'}, annot=True)

    plt.ylim(0, 6)
    plt.yticks(rotation=0, fontsize=15)
    plt.xticks(rotation=0, fontsize=15)
    plt.xlabel('Zvolená emoce')
    plt.ylabel('Číslo prezentace')
    plt.savefig('{}/heatmap_emotion_choice.png'.format(path))

    f.clear()
    plt.cla()
    plt.clf()


def hr_eda_stat(path):
    """
        Plot and print heart rate (HR), heart rate variability (HRV),
        electrodermal activity (EDA) statistics. Specially Mean and Std values
        of these signal components.

        Parameters
        ----------

        path : str
            Path where data are stored.

    """

    dataset = pd.DataFrame()
    base = pd.DataFrame()
    hrv = pd.DataFrame()
    for folder, neutral_df, emotion_df in load_data(path):
        zero_neutral = neutral_df.loc[neutral_df['id'] == 0]
        neutral_df = neutral_df.loc[neutral_df['id'] != 0]
        if base.empty:
            base = zero_neutral.copy()
        else:
            base = pd.concat([base, zero_neutral])

        if dataset.empty:
            dataset = emotion_df.copy()
            dataset = pd.concat([dataset, neutral_df])
        else:
            dataset = pd.concat([dataset, emotion_df, neutral_df])

        hrv_data = pd.read_csv('{}/{}/hrv.csv'.format(path, folder))
        if hrv.empty:
            hrv = hrv_data.copy()
        else:
            hrv = pd.concat([hrv, hrv_data])

    #HR to Phasic

    ppg_rate = dataset[['PPG_Rate', 'Condition']]
    ppg_rate_grouped = ppg_rate.groupby('Condition')
    ppg_rate_mean = ppg_rate_grouped.mean()
    ppg_rate_std = ppg_rate_grouped.std()

    print('\nHear Rate Statistic')
    print('----------------------------------------')
    print('HR Mean: \n{}'.format(ppg_rate_mean))
    print('HR Std: \n{}'.format(ppg_rate_std))
    print('----------------------------------------')

    eda = dataset[['EDA_Phasic', 'Condition']]
    eda_grouped = eda.groupby('Condition')
    eda_mean = eda_grouped.mean()
    eda_std = eda_grouped.std()

    print('\nEDA Phasic Statistic')
    print('----------------------------------------')
    print('EDA Mean: \n{}'.format(eda_mean))
    print('EDA Std: \n{}'.format(eda_std))
    print('----------------------------------------')

    rate_mean_change = ppg_rate_mean - base['PPG_Rate'].mean()
    rate_std_change = ppg_rate_std - base['PPG_Rate'].std()
    print('\nHear Rate Mean Change')
    print('----------------------------------------')
    print('HR Mean: \n{}'.format(rate_mean_change))
    print('HR Std: \n{}'.format(rate_std_change))
    print('----------------------------------------')

    eda_mean_change = eda_mean - base['EDA_Phasic'].mean()
    eda_std_change = eda_std - base['EDA_Phasic'].std()
    print('\nEDA Phasic Mean Change')
    print('----------------------------------------')
    print('EDA Mean: \n{}'.format(eda_mean_change))
    print('EDA Std: \n{}'.format(eda_std_change))
    print('----------------------------------------')

    rate_phasic_mean = (pd.concat([ppg_rate_mean, eda_mean], axis=1)).reset_index()

    g = sns.lmplot(data=rate_phasic_mean, x='PPG_Rate', y='EDA_Phasic',
                    hue='Condition', legend=True)
    sns.despine(top=False, right=False, left=False, bottom=False)

    new_title = 'Emoce'
    g._legend.set_title(new_title)
    new_labels = ['klidový stav', 'nuda',
                  'pozitivní', 'radost',
                  'strach', 'zmatek',
                  'znechucení']

    for t, l in zip(g._legend.texts, new_labels): t.set_text(l)

    plt.xlabel('Srdeční tep [úderů/min]')
    plt.ylabel('Fázová reakce (EDA) [uS]')
    plt.savefig('{}/rate_to_phasic.png'.format(path))

    plt.cla()
    plt.clf()

    #HRV to Phasic

    hrv = hrv.fillna(0)

    hrv_mean = hrv.loc[hrv['type'] == 'base'].copy()

    hrv_base_grouped = hrv.loc[hrv['type'] == 'base'].groupby('Condition')
    hrv_base_mean = hrv_base_grouped.mean()

    hrv_emotion_grouped = hrv.loc[hrv['type'] == 'stimul'].groupby('Condition')
    hrv_emotion_mean = hrv_emotion_grouped.mean()
    hrv_emotion_mean = hrv_emotion_mean.reset_index()

    hrv_mean['Condition'] = 'neutral'
    hrv_mean = pd.concat([hrv_mean, hrv_emotion_mean])
    hrv_mean = hrv_mean.groupby('Condition').mean()

    hrv_phasic = pd.concat([hrv_mean, eda_mean], axis=1).reset_index()

    g = sns.lmplot(data=hrv_phasic, x='HRV_MeanNN', y='EDA_Phasic', hue='Condition')

    new_title = 'Emoce'
    g._legend.set_title(new_title)
    new_labels = ['klidový stav', 'nuda',
                  'pozitivní', 'radost',
                  'strach', 'zmatek',
                  'znechucení']

    for t, l in zip(g._legend.texts, new_labels): t.set_text(l)
    sns.despine(top=False, right=False, left=False, bottom=False)
    plt.xlabel('Variabilita srdečního tepu [ms]')
    plt.ylabel('Fázová reakce (EDA) [uS]')
    plt.xlim(780, 960)
    plt.savefig('{}/hrv_phasic_mean.png'.format(path))

    plt.show()
    plt.cla()
    plt.clf()



if __name__ == '__main__':
    path = os.path.dirname(os.getcwd())
    path = '{}/data'.format(path)

    emotion_gender_df = pd.read_csv('{}/Emotion_Gender.csv'.format(path))
    hr_eda_stat(path)
    plot_stat(path, emotion_gender_df)
    plot_heatmap_emotion_choice(path)
    get_mean_hrv_indices(path)
