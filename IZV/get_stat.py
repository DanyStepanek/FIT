from download import DataDownloader
import numpy as np
import matplotlib as mp

def get_data_for_years(data_source):
    data = data_source[1]

    datetimes = data[data_source[0].index('p2a')]
    regions = data[data_source[0].index('region')]

    regions_names = set(regions)
    years_regions_data_count = dict()

    for i in range(len(data[0])):
        year = str(np.datetime64(datetimes[i], 'Y'))
        if year not in years_regions_data_count.keys():
            years_regions_data_count[year] = dict.fromkeys(regions_names, 0)
        years_regions_data_count[year][regions[i]] += 1

    return years_regions_data_count


def plot_stat(data_source, fig_location=None, show_figure=False):

    years_data = get_data_for_years(data_source)

    for year, regions in years_data.items():
        print(year)
        for k, v in regions.items():
            print('{} : {}'.format(k, v))


    #save to file
    if fig_location:
        pass

    #plot graph
    if show_figure:
        pass



data_source = DataDownloader().get_list(['ZLK', 'JHM', 'OLK'])
plot_stat(data_source)
