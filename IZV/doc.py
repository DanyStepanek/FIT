# Jaka je hlavni pricina nehody s ohledem na druh pozemni komunikace (
#dalnice,  silnice I. - III. tridy).
# S hypotezou, ze ma charakter vliv na hlavni pricinu nehody.

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

"""
    Read pickle file and return data as DataFrame.
"""
def get_data(filename='accidents.pkl.gz'):
    df = pd.read_pickle(filename)
    return df

"""
    Print data used in the document.
"""
def print_data(acc_df):
    #sum of all accidents
    count = acc_df['count'].sum()

    injury = acc_df[acc_df['character'] == 1]
    injury_count = injury['count'].sum()

    non_injury = acc_df[acc_df['character'] == 2]
    non_injury_count = count - injury_count

    print('Pocet nehod celkem: {}'.format(count))
    print('Pocet nehod se zranenim: {}'.format(injury_count))
    print('Pocet nehod bez zraneni: {}'.format(non_injury_count))
    print('\n')

    roads = ['dalnice\t\t', 'silnice I. tridy',
             'silnice II. tridy', 'silnice III. tridy']

    print('Nehody se zranenim')
    print('Typ\t\t\tHlavni pricina\t\t\tPocet nehod')
    for i in range(0, 4):
        max = (injury[injury['road_type'] == i])['count'].max()
        main_cause = injury.loc[injury['count'] == max, 'cause_info'].item()
        print('{}\t{}\t\t{}'.format(roads[i], main_cause, max))

    print('\n')

    print('Nehody bez zraneni')
    print('Typ\t\t\tHlavni pricina\t\t\tPocet nehod')
    for i in range(0, 4):
        max = (non_injury[non_injury['road_type'] == i])['count'].max()
        main_cause = non_injury.loc[non_injury['count'] == max, 'cause_info'].item()
        print('{}\t{}\t\t{}'.format(roads[i], main_cause, max))


"""
    Function for hypothesis validation.
"""
def get_stat(acc_df):
    acc_df = acc_df[['character', 'cause_info', 'count']]

    #Sum of accidents grouped by character and cause of the accident
    acc_stat = acc_df.groupby(['character', 'cause_info']).agg('sum')
    acc_stat = acc_stat.reset_index()


    print('Overeni hypotezy')
    char_label = {1 : 'se zranenim', 2 : 'pouze hmotna skoda'}

    #find and print main cause for character of the accident.
    for i in range(1, 3):
        character = acc_stat[acc_stat['character'] == i]
        max = character['count'].max()
        main_cause = character.loc[character['count'] == max, 'cause_info'].item()

        print('Typ: {} Pricina: {} Pocet: {}'.format(char_label[i], main_cause, max))
    print('\n')

"""
    Plot categorical graph for each character of the accident. Data are divided
    by the type of road and by cause of the accident.
"""
def plot_road(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False, show_data: bool = False):

    #new dataframe
    acc_df = df[['p36', 'p12', 'p9']].rename(
                    columns={'p36' : 'road_type', 'p12' : 'cause', 'p9' : 'character'})

    #clear dataframe
    acc_df = acc_df.dropna()

    #retype str -> int
    columns = ['road_type', 'cause', 'character']
    for col in columns:
        acc_df[col] = acc_df[col].astype('int')


    #roads I. - III. class and highways
    acc_df = acc_df[acc_df['road_type'] <= 3]

    #cause to classes
    bins = pd.IntervalIndex.from_tuples([(99, 100), (200, 209), (300, 311),
                                         (400, 414), (500, 516), (600, 615)])

    labels = ["nezavinena ridicem", "neprimerena rychlost jizdy", "nespravne predjizdeni",
              "nedani prednosti v jizde", "nespravny zpusob jizdy", "technicka zavada vozidla"]

    acc_df['cause_info'] = pd.cut(acc_df['cause'], bins=bins).map(dict(zip(bins, labels)))

    #add column for count of accidents
    acc_df['count'] = 1

    #count of accidents separeted by character of accident, type  of road and by cause
    acc_grouped = acc_df.groupby(['character', 'road_type', 'cause_info']).agg('count')
    acc_counted = acc_grouped.reset_index()

    #hypothesis validation
    get_stat(acc_counted)

    #visualization
    palette = 'magma'
    g = sns.catplot(x='road_type', y="count", hue='cause_info',
                    col='character', col_wrap=2,
                    data=acc_counted, kind="bar", log=True,
                    saturation=1.5, aspect=1, height=5, palette=palette)

    road_labels = ['D', 'I.tr', 'II.tr', 'III.tr']
    g.set_xticklabels(road_labels)
    g.fig.subplots_adjust(top=0.8, bottom=0.1)
    g.fig.suptitle('Příčina nehody dle úrovně pozemní komunikace')
    g.set_axis_labels("Úroveň pozemní komunikace", "Počet nehod")
    g._legend.set_title('Příčina nehody')
    new_labels = ["nezaviněná řidičem", "nepřiměřená rychlost jízdy", "nesprávné předjíždění",
              "nedání přednosti v jízdě", "nesprávný způsob jízdy", "technická závada vozidla"]
    zip(g._legend.texts, new_labels)
    for t, l in zip(g._legend.texts, new_labels): t.set_text(l)

    #set title for subplots
    for ax, title in zip(g.axes.flat, ['se zraněním', 'pouze hmotná škoda']):
        ax.set_title(title)

    #show table and important data
    if show_data:
        print_data(acc_counted)

    #save graph to file
    if fig_location:
        g.savefig(fig_location)

    #plot graph
    if show_figure:
        plt.show()

if __name__ == '__main__':
    df = get_data()
    plot_road(df, fig_location='fig.png', show_figure=False, show_data=True)
