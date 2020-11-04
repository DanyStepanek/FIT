from download import DataDownloader
import numpy as np
import matplotlib
import argparse
import os
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def save_graph_to_file(fig_location, fig):
    dir = os.path.dirname(fig_location)
    file = os.path.basename(fig_location)
    file_ext = file.split('.')[1]

    fcb = matplotlib.backends.backend_agg.FigureCanvasBase(fig)
    supported_file_types = fcb.get_supported_filetypes()
    if file_ext in supported_file_types.keys():
        os.makedirs(dir, exist_ok=True)
        fig.savefig('{}/{}'.format(dir, file))
    else:
        raise ValueError('File type ({}) is not supported.'.format(file_ext))



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

#https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/barchart.html
def autolabel(ax, rects, order):
    """Attach a text label in each bar in *rects*, displaying its height."""
    for rect, index in zip(rects, order):
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, 0),
                    xytext=(0, 0),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=7, color='white')

        """Attach a text label above each bar in *rects*, displaying its order."""
        ax.annotate('{}.'.format(index + 1),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 0),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, color='black')


def plot_stat(data_source, fig_location=None, show_figure=False):

    years_data = get_data_for_years(data_source)

    years = list(years_data.keys())
    regions = list(years_data.values())

    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(nrows=5, ncols=1,
                                    constrained_layout=True, figsize=(9, 9))
    fig.suptitle('Statistika nehod v letech 2016-2020')

    y_2016 = years_data['2016']
    y_2017 = years_data['2017']
    y_2018 = years_data['2018']
    y_2019 = years_data['2019']
    y_2020 = years_data['2020']

    y_2016_values = list(y_2016.values())
    y_2017_values = list(y_2017.values())
    y_2018_values = list(y_2018.values())
    y_2019_values = list(y_2019.values())
    y_2020_values = list(y_2020.values())


    region_names = list(y_2016.keys())

    width = 0.6
    color = 'darkslategrey'
    xlabel = 'Kraje'
    ylabel = 'Pocet nehod'
    yscale = 'linear'
    yticks = [0, 5000, 10000, 15000, 20000, 25000, 30000]
    font = {'size' : 8, 'family' : 'Times New Roman', 'rotation' : 0, 'color' : 'black'}

    rects = ax1.bar(region_names, y_2016_values, width, color=color)
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_yscale(yscale)
    ax1.set_yticks([ val for val in range(0, max(y_2016_values) + 5000, 5000)])
    ax1.set_yticklabels(yticks, rotation=font['rotation'], fontsize=font['size'])
    ax1.grid(axis='y', linestyle='-', linewidth='0.2', color='grey')
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.set_title('2016')

    sorted_values = sorted(y_2016_values, reverse=True)
    indexed_order = [sorted_values.index(i) for i in y_2016_values]

    autolabel(ax1, rects, indexed_order)

    rects = ax2.bar(region_names, y_2017_values, width, color=color)
    ax2.set_xlabel(xlabel)
    ax2.set_ylabel(ylabel)
    ax2.set_yscale(yscale)
    ax2.set_yticks([ val for val in range(0, max(y_2017_values) + 5000, 5000)])
    ax2.set_yticklabels(yticks, rotation=font['rotation'], fontsize=font['size'])
    ax2.grid(axis='y', linestyle='-', linewidth='0.2', color='grey')
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.set_title('2017')

    sorted_values = sorted(y_2017_values, reverse=True)
    indexed_order = [sorted_values.index(i) for i in y_2017_values]

    autolabel(ax2, rects, indexed_order)

    rects = ax3.bar(region_names, y_2018_values, width, color=color)
    ax3.set_xlabel(xlabel)
    ax3.set_ylabel(ylabel)
    ax3.set_yscale(yscale)
    ax3.set_yticks([ val for val in range(0, max(y_2018_values) + 5000, 5000)])
    ax3.set_yticklabels(yticks, rotation=font['rotation'], fontsize=font['size'])
    ax3.grid(axis='y', linestyle='-', linewidth='0.2', color='grey')
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.set_title('2018')

    sorted_values = sorted(y_2018_values, reverse=True)
    indexed_order = [sorted_values.index(i) for i in y_2018_values]

    autolabel(ax3, rects, indexed_order)

    rects = ax4.bar(region_names, y_2019_values, width, color=color)
    ax4.set_xlabel(xlabel)
    ax4.set_ylabel(ylabel)
    ax4.set_yscale(yscale)
    ax4.set_yticks([ val for val in range(0, max(y_2019_values) + 5000, 5000)])
    ax4.set_yticklabels(yticks, rotation=font['rotation'], fontsize=font['size'])
    ax4.grid(axis='y', linestyle='-', linewidth='0.2', color='grey')
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    ax4.set_title('2019')

    sorted_values = sorted(y_2019_values, reverse=True)
    indexed_order = [sorted_values.index(i) for i in y_2019_values]

    autolabel(ax4, rects, indexed_order)

    rects = ax5.bar(region_names, y_2020_values, width, color=color)
    ax5.set_xlabel(xlabel)
    ax5.set_ylabel(ylabel)
    ax5.set_yscale(yscale)
    ax5.set_yticks([ val for val in range(0, max(y_2020_values) + 5000, 5000)])
    ax5.set_yticklabels(yticks, rotation=font['rotation'], fontsize=font['size'])
    ax5.grid(axis='y', linestyle='-', linewidth='0.2', color='grey')
    ax5.spines["top"].set_visible(False)
    ax5.spines["right"].set_visible(False)
    ax5.set_title('2020')

    sorted_values = sorted(y_2020_values, reverse=True)
    indexed_order = [ sorted_values.index(i) for i in y_2020_values]

    autolabel(ax5, rects, indexed_order)

    #save graph to file
    if fig_location:
        save_graph_to_file(fig_location, fig)

    #plot graph
    if show_figure:
        plt.show()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fig_location')
    parser.add_argument('--show_figure', action='store_true')

    args = vars(parser.parse_args())

    data_source = DataDownloader().get_list()
    plot_stat(data_source, show_figure=args['show_figure'], fig_location=args['fig_location'])
