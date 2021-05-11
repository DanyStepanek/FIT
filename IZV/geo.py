#!/usr/bin/python3.8
# coding=utf-8
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster as cluster
import numpy as np
# muzeze pridat vlastni knihovny

def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """ Konvertovani dataframe do geopandas.GeoDataFrame se spravnym kodovani"""

    clear_df = df.dropna(subset=['d', 'e'])
    return geopandas.GeoDataFrame(clear_df,
                                 geometry=geopandas.points_from_xy(clear_df['d'], clear_df['e']),
                                 crs='epsg:5514')

def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """ Vykresleni grafu s dvemi podgrafy podle lokality nehody """

    epsg_web_mercator = 'epsg:3857'

    fig, axs = plt.subplots(1, 2, figsize=(16, 9))
    fig.suptitle('Zlinsky kraj')

    zlk_gdf = gdf[gdf['region'] == 'ZLK']
    zlk_gdf = zlk_gdf.to_crs(epsg_web_mercator)

    axs[0].set_title('Nehody v obci')
    zlk_gdf[zlk_gdf['p5a'] == 1].plot(ax=axs[0], color='purple', marker=".", markersize=40)

    axs[1].set_title('Nehody mimo obec')
    zlk_gdf[zlk_gdf['p5a'] == 2].plot(ax=axs[1], color='green', marker=".", markersize=40)

    ctx.add_basemap(axs[0],crs=epsg_web_mercator,
                    source=ctx.providers.Stamen.TonerLite,alpha=0.9)

    ctx.add_basemap(axs[1],crs=epsg_web_mercator,
                    source=ctx.providers.Stamen.TonerLite,alpha=0.9)


    fig.axes[0].get_xaxis().set_visible(False)
    fig.axes[0].get_yaxis().set_visible(False)
    fig.axes[1].get_xaxis().set_visible(False)
    fig.axes[1].get_yaxis().set_visible(False)

    if fig_location:
        fig.savefig(fig_location)

    if show_figure:
        plt.show()



def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """ Vykresleni grafu s lokalitou vsech nehod v kraji shlukovanych do clusteru """

    epsg_web_mercator = 'epsg:3857'

    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    fig.suptitle('Nehody ve Zlinskem kraji')

    zlk_gdf = gdf[gdf['region'] == 'ZLK']

    kmeans = cluster.MiniBatchKMeans(n_clusters=20)
    kmcls = kmeans.fit(zlk_gdf[['d', 'e']])

    centers = kmcls.cluster_centers_
    labels = kmcls.labels_

    data = {'centers_x' : centers[:,0],
            'centers_y' : centers[:,1],
            'count' : np.bincount(labels)
           }

    zlk_df = pd.DataFrame(data, columns=['centers_x', 'centers_y', 'count'])
    zlk_cls_gdf = geopandas.GeoDataFrame(zlk_df,
                        geometry=geopandas.points_from_xy(zlk_df['centers_x'], zlk_df['centers_y']),
                        crs='epsg:5514')

    zlk_gdf = zlk_gdf.to_crs(epsg_web_mercator)
    zlk_gdf.plot(ax=ax, color="purple", marker=".", markersize=5)

    zlk_cls_gdf = zlk_cls_gdf.to_crs(epsg_web_mercator)
    zlk_cls_gdf = zlk_cls_gdf.sort_values('count')

    zlk_cls_gdf.plot(ax=ax, column='count', marker='o',
                     markersize=zlk_cls_gdf['count'],
                     alpha=.5, legend=True, cmap='winter',
                     legend_kwds={'label': "Pocet nehod",
                                  'orientation': "vertical"})

    ctx.add_basemap(ax,crs=epsg_web_mercator,
                    source=ctx.providers.Stamen.TonerLite,alpha=0.9)

    if fig_location:
        fig.savefig(fig_location)

    if show_figure:
        plt.show()

if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    plot_geo(gdf, "geo1.png", False)
    plot_cluster(gdf, "geo2.png", False)
