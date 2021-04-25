
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from file_processing import get_data

plt.rcParams['figure.figsize'] = [10, 6]
plt.rcParams['font.size']= 18

def plot_stat(path, emotion_gender_df, show_fig=False):
    f = sns.histplot(data=emotion_gender_df,
                     x='emotion', binwidth=5)
    f.set_xlabel('Emoce')
    f.set_ylabel('Počet')
    f.yaxis.set_major_locator(MaxNLocator(integer=True))
    f.set_xticklabels(['Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])
#    f.set_title('Histogram získaných vzorků')
    handles, _ = f.get_legend_handles_labels()
    f.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}\\hist.png'.format(path))

    if show_fig:
        plt.show()

    f.clear()
    plt.cla()
    plt.clf()
#    plt.close(f)

    g = sns.countplot(data=emotion_gender_df,
                      x='emotion', hue="gender")
    g.set_xlabel('Emoce')
    g.set_ylabel('Počet')
    g.yaxis.set_major_locator(MaxNLocator(integer=True))
    g.set_xticklabels(['Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])
#    g.set_title('Počet vzorků kategorizovaný podle pohlaví')
    handles, _ = g.get_legend_handles_labels()
    g.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}\\emotion_count.png'.format(path))

    if show_fig:
        plt.show()

    g.clear()
    plt.cla()
    plt.clf()
#    plt.close(g)

def plot_features(path, erf_df, show_fig=False):
    f = sns.boxplot(x='Condition', y='PPG_Rate', hue='Gender', data=erf_df)
    f.set_xlabel('Emoce')
    f.set_ylabel('Rozdíl středních hodnot tepu [bpm]')
    f.yaxis.set_major_locator(MaxNLocator(integer=True))
    f.set_xticklabels(['Neutrální', 'Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])
#    f.set_title('Změna srdečního tepu při reakci na podnět')
    handles, _ = f.get_legend_handles_labels()
    f.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}\\heart_rate.png'.format(path))

    if show_fig:
        plt.show()

    f.clear()
    plt.cla()
    plt.clf()
#    plt.close(f)


    g = sns.boxplot(x='Condition', y='EDA_Tonic', hue='Gender', data=erf_df)
    g.set_xlabel('Emoce')
    g.set_ylabel('EDA tónická složka [uS]')
    g.yaxis.set_major_locator(MaxNLocator(integer=True))
    g.set_xticklabels(['Neutrální', 'Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])
    #g.set_title('Změna tónické složky EDA při reakci na podnět')
    handles, _ = g.get_legend_handles_labels()
    g.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}\\eda_tonic.png'.format(path))

    if show_fig:
        plt.show()

    g.clear()
    plt.cla()
    plt.clf()
#    plt.close(g)

    h = sns.boxplot(x='Condition', y='EDA_Phasic', hue='Gender', data=erf_df)
    h.set_xlabel('Emoce')
    h.set_ylabel('EDA fázická složka [uS]')
    h.yaxis.set_major_locator(MaxNLocator(integer=True))
    h.set_xticklabels(['Neutrální', 'Nuda', 'Pozitivní', 'Radost', 'Strach', 'Zmatek', 'Znechucení'])
    #h.set_title('Změna fázické složky EDA při reakci na podnět')
    handles, _ = h.get_legend_handles_labels()
    h.legend(handles, ['Muži', 'Ženy'], loc="best") # Associate
    plt.savefig('{}\\eda_phasic.png'.format(path))

    if show_fig:
        plt.show()

    h.clear()
    plt.cla()
    plt.clf()
#    plt.close(h)

def plot_ppg(path, folder, neutral_ppg, emotion_ppg):
    fig, axs = plt.subplots(nrows=1, ncols=2, sharey=True, constrained_layout=True)
    emotion = folder.split('_')[0]
    fig.suptitle('neutrální - {}'.format(emotion))

    ax0 = sns.lineplot(ax=axs[0], x='index1', y='PPG_Rate', hue='id', data=neutral_ppg)
    ax0.set_xlabel('Vzorek [n]')
    ax0.set_ylabel('Srdeční tep [bpm]')

    ax1 = sns.lineplot(ax=axs[1], x='index1', y='PPG_Rate', hue='id', data=emotion_ppg)
    ax1.set_xlabel('Vzorek [n]')
    ax1.set_ylabel('Srdeční tep [bpm]')

    plt.savefig('{}\\{}\\heart_rate_compilation.png'.format(path, folder))

    fig.clear()
    plt.close(fig)

def plot_eda(path, folder, neutral_eda, emotion_eda):
    fig, axs = plt.subplots(nrows=2, ncols=2, sharey=True, sharex=True, constrained_layout=True)
    emotion = folder.split('_')[0]
    fig.suptitle('neutrální - {}'.format(emotion))

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

    plt.savefig('{}\\{}\\eda_compilation.png'.format(path, folder))

    fig.clear()
    plt.close(fig)

def plot_signals_for_all_epochs_by_emotion(path):
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
    folders = os.listdir(path)

    for folder in folders:
        folder_path = '{}\\{}'.format(path, folder)

        if os.path.isdir(folder_path):
            neutral_df = pd.read_csv('{}\\{}\\epochs\\neutral_all.csv'.format(path, folder))
            emotion_df = pd.read_csv('{}\\{}\\epochs\\emotion_all.csv'.format(path, folder))
            yield folder, neutral_df, emotion_df

def dataset_stat(samples_count=0, folders_count=0):
    print('\nDataset Statistic')
    print('----------------------------------------')
    print('Samples count: {}'.format(samples_count))
    print('Folders count: {}'.format(folders_count))
    print('----------------------------------------')




def heart_rate_stat(path):
    dataset = pd.DataFrame()

    for _, _, emotion_df in load_data(path):
        if dataset.empty:
            dataset = emotion_df.copy()
        else:
            dataset = pd.concat([dataset, emotion_df])

    ppg_rate = dataset[['PPG_Rate', 'Condition']]
    ppg_rate_grouped = ppg_rate.groupby('Condition')
    ppg_rate_mean = ppg_rate_grouped.mean()
    ppg_rate_std = ppg_rate_grouped.std()

    print('\nHear Rate Statistic')
    print('----------------------------------------')
    print('HR Mean: {}'.format(ppg_rate_mean))
    print('HR Std: {}'.format(ppg_rate_std))
    print('----------------------------------------')




if __name__ == '__main__':
    path = '.\\data'
    #plot_signals_for_all_epochs_by_emotion(path)
    heart_rate_stat(path)
