#!/usr/bin/env python3.8
# coding=utf-8

import matplotlib
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns
import numpy as np
import os
import gzip, pickle
# muzete pridat libovolnou zakladni knihovnu ci knihovnu predstavenou na prednaskach
# dalsi knihovny pak na dotaz



def get_memory_usage(df):
    # 1 MB = 1 048 576 B
    return df.memory_usage(deep=True).sum() / 1048576


# Ukol 1: nacteni dat
def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    #unpack gzip and load data
    with gzip.open(filename, 'rb') as fd:
        p = pickle.Unpickler(fd)
        df = p.load()

    #add column date
    df['date'] = pd.Series( d for d in df['p2a'] ).astype('datetime64')

    orig_size = get_memory_usage(df)

    #retype columns
    cols = df.columns.tolist()
    for item in ['p1', 'region']:
        cols.remove(item)

    for col in cols:
        df[col] = df[col].astype('category')

    new_size = get_memory_usage(df)

    #print memory usage
    if verbose:
        print('orig_size={:.1f} MB'.format(orig_size))
        print('new_size={:.1f} MB'.format(new_size))

    return df

#https://stackoverflow.com/questions/43214978/seaborn-barplot-displaying-values
def annotate_barplot(ax):
    for b in ax.patches:
        ax.annotate(format(b.get_height(), '.0f'),
                   (b.get_x() + b.get_width() / 2., b.get_height()),
                   ha = 'center', va = 'center', fontsize=8, color='white',
                   xytext = (0, -7),
                   textcoords = 'offset points')
    return ax

# Ukol 2: následky nehod v jednotlivých regionech
def plot_conseq(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):
    sns.set()
    sns.set_style("darkgrid")

    fig, axs = plt.subplots(nrows=4, ncols=1,
                                    constrained_layout=True, figsize=(9, 9))
    fig.suptitle('Nasledky nehod v jednotlivych regionech')

    conseq_df = df[ ['p13a', 'p13b', 'p13c', 'region'] ].rename(
                            columns={'p13a' : 'death', 'p13b' : 'serious', 'p13c' : 'light'} )

    conseq_df['death'] = conseq_df['death'].astype('int64')
    conseq_df['serious'] = conseq_df['serious'].astype('int64')
    conseq_df['light'] = conseq_df['light'].astype('int64')

    conseq_grouped = conseq_df.groupby('region')
    conseq_to_plot = conseq_grouped.sum()
    conseq_to_plot['count'] = conseq_grouped['death'].count()
    conseq_to_plot = conseq_to_plot.reset_index()

    palette = "winter"
    ax0 = sns.barplot(ax=axs[0], x="region", y="count", data=conseq_to_plot, palette=palette,
                order=conseq_to_plot.sort_values('count', ascending=False).region)
    ax1 = sns.barplot(ax=axs[1], x="region", y="light", data=conseq_to_plot, palette=palette,
                order=conseq_to_plot.sort_values('count', ascending=False).region)
    ax2 = sns.barplot(ax=axs[2], x="region", y="serious", data=conseq_to_plot, palette=palette,
                order=conseq_to_plot.sort_values('count', ascending=False).region)
    ax3 = sns.barplot(ax=axs[3], x="region", y="death", data=conseq_to_plot, palette=palette,
                order=conseq_to_plot.sort_values('count', ascending=False).region)

    annotate_barplot(ax0)
    annotate_barplot(ax1)
    annotate_barplot(ax2)
    annotate_barplot(ax3)

    #save graph to file
    if fig_location:
        fig.savefig(fig_location)

    #plot graph
    if show_figure:
        plt.show()

# Ukol3: příčina nehody a škoda
def plot_damage(df: pd.DataFrame, fig_location: str = None,
                show_figure: bool = False):

    damage_df  = df[ ['p53', 'p12', 'region'] ].rename(
                            columns={'p53' : 'damage', 'p12' : 'cause'} )

    damage_df['damage'] = damage_df['damage'].astype('int64').div(10)
    damage_df['cause'] = damage_df['cause'].astype('int64')

    damage_df = damage_df[ damage_df['region'].isin(['ZLK', 'JHM', 'HKK', 'OLK']) ]

    #cut cause to classes
    bins = pd.IntervalIndex.from_tuples([(99, 100), (200, 209), (300, 311),
                                         (400, 414), (500, 516), (600, 615)])
    labels = ["nezavinena_ridicem", "neprimerena_rychlost_jizdy", "nespravne_predjizdeni",
              "nedani prednosti_v_jizde", "nespravny_zpusob_jizdy", "technicka_zavada_vozidla"]

    damage_df['cause_info'] = pd.cut(damage_df['cause'], bins=bins).map(dict(zip(bins, labels))                                       )

    #cut damage to classes
    bins = pd.IntervalIndex.from_tuples([(-1, 50), (50, 200), (200, 500),
                                         (500, 1000), (1000, np.inf)])
    labels = ["< 50", "50 - 200", "200 - 500", "500 - 1000", ">1000"]
    damage_df['damage_category'] = pd.cut(damage_df['damage'], bins=bins).map(dict(zip(bins, labels)))

    sns.set()
    sns.set_style("darkgrid")

    g = sns.catplot(x="damage_category", y="damage", hue='cause_info', col="region", col_wrap=2,
                data=damage_df, kind="bar", log=True, saturation=1.5, aspect=1,
                height=5)

    g.fig.subplots_adjust(top=0.9, bottom=0.1)
    g.fig.suptitle('Pricina nehody a skoda')
    g.fig.subplots_adjust(wspace=0.2, hspace=0.2)
    g.set_axis_labels("Skoda v tis. [Kc]", "Pocet nehod")
    g.set_xticklabels(labels)
    g.set_titles("{col_name}")
    g._legend.set_title('Pricina nehody')

    new_labels = ["nezavinena ridicem", "neprimerena rychlost jizdy", "nespravne predjizdeni",
              "nedani prednosti v jizde", "nespravny zpusob jizdy", "technicka zavada vozidla"]
    for t, l in zip(g._legend.texts, new_labels): t.set_text(l)

    #save graph to file
    if fig_location:
        g.savefig(fig_location)

    #plot graph
    if show_figure:
        plt.show()

# Ukol 4: povrch vozovky
def plot_surface(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):


    surface_df  = df[ ['p16', 'date', 'region'] ].rename(columns={'p16' : 'road_state'})

    #category type to int
    surface_df['road_state'] = surface_df['road_state'].astype('int64')

    #get 4 regions
    surface_df = surface_df[ surface_df['region'].isin(['ZLK', 'JHM', 'HKK', 'OLK']) ]

    #category type to datetime
    surface_df['date'] = pd.to_datetime(surface_df['date'])

    #crosstab: index [region, date.(year, month)], columns [road state]
    surface_crosstab = pd.crosstab([surface_df['region'], surface_df['date'].apply(lambda x: x.strftime('%Y-%m'))],
                                    columns=surface_df['road_state'])

    surface_crosstab = surface_crosstab.rename(columns={0 : 'jine', 1 : 'suchy_cisty',
                            2 : 'suchy_znecisteny', 3 : 'mokry',
                            4 : 'blato', 5 : 'led_ujety_snih_posyp', 6 : 'led_ujety_snih',
                            7 : 'unik_kapalin', 8 : 'cerstvy_snih', 9 : 'nahla_zmena'})

    surface_crosstab_stack = surface_crosstab.stack().reset_index()
    surface_crosstab_stack = surface_crosstab_stack.rename(columns={0 : 'count'})

    sns.set()
    sns.set_style("darkgrid")
    palette = "Set2"

    g = sns.relplot(data=surface_crosstab_stack, col='region', hue='road_state', col_wrap=2,
                    x='date', y='count', kind='line', palette=palette, aspect=1.5,
                    height=5)

    g.fig.subplots_adjust(top=0.9, bottom=0.1)
    g.fig.suptitle('Stav vozovky v jednotlivých měsících')
    g.fig.subplots_adjust(wspace=0.01, hspace=0.1)
    g.set_axis_labels("Mesic", "Pocet nehod")
    g.set_titles("{col_name}")

    #https://stackoverflow.com/questions/43727278/how-to-set-readable-xticks-in-seaborns-facetgrid
    year_labels = ['2016', '2017', '2018', '2019', '2020']
    for ax in g.axes.flat:
        labels = ax.get_xticklabels() # get x labels
        for i,l in enumerate(labels):
            #replace months by year labels
            if(i % 12 == 0):
                labels[i] = year_labels[i // 12]
            else:
                labels[i] = ''
        ax.set_xticklabels(labels, rotation=30, size=10) # set new labels

    g._legend.set_title('Stav vozovky')
    new_labels = ['jiny', 'sucha cista', 'sucha znecistena', 'mokra',
                  'blato', 'led, ujety snih, posyp', 'led, ujety snih',
                  'unikla kapalina', 'cerstvy snih', 'nahla zmena stavu']

    for t, l in zip(g._legend.texts, new_labels): t.set_text(l)

    #save graph to file
    if fig_location:
        g.savefig(fig_location)

    #plot graph
    if show_figure:
        plt.show()


if __name__ == "__main__":
    pass
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce.
    df = get_dataframe("accidents.pkl.gz", verbose=True)
    plot_conseq(df, fig_location="01_nasledky.png", show_figure=False)
    plot_damage(df, "02_priciny.png", show_figure=False)
    plot_surface(df, "03_stav.png", show_figure=False)
