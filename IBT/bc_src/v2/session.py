# -*- coding: utf-8 -*-
"""

@author: Daniel Stepanek
"""

import argparse
import os

from client import Client
from data_convertor import load_files, raw_data_to_csv
from visualize import get_data, plot_data

from pathlib import Path

def str_to_int(string):
    try:
        num = int(string)
        return num
    except ValueError:
        return False


def set_emotion_and_gender_to_received_data(path, filename):
    emotion_dict = {1 : 'nuda', 2 : 'pozitivni', 3 : 'radost',
                    4 : 'strach', 5 : 'zmatek', 6 : 'znechuceni'}
    print('Vyber prosim odpovidajici emoci (1 - 6):')
    for k, v in emotion_dict.items():
        print('{}. {}'.format(k, v))

    while True:
        emotion = input()
        e_index = str_to_int(emotion)
        if e_index:
            if e_index >= 1 and e_index <= 6:
                break

        print('Nevalidni vstup ({}).'.format(emotion))
        print('Zadej cislo v rozsahu 1 - 6.')

    gender_dict = {1 : 'muz', 2 : 'zena'}
    print('Vyber prosim sve pohlavi (1, 2):')
    for k, v in gender_dict.items():
        print('{}. {}'.format(k, v))

    while True:
        gender = input()
        g_index = str_to_int(gender)
        if g_index:
            if g_index == 1 or g_index == 2:
                break

        print('Nevalidni vstup ({}).'.format(gender))
        print('Zadej cislo 1 nebo 2.')

    print('V poradku, dekuji za spolupraci. :)')

    new_filename = '{}{}_{}'.format(emotion_dict[e_index], filename, gender_dict[g_index])
    os.rename('{}\\{}.txt'.format(path, filename),
              '{}\\{}.txt'.format(path, new_filename))


"""
    Connect to server.
    Receive data until Enter is pressed.
    Convert raw data to dataframe and store as csv files. (./data)
    Plot data for each experiment. (./plots)
"""
def session(path, keep_raw_data, fig):
    client = Client()
    client.connect()
    filename = client.filename

    p_data = '{}\\data'.format(path)
    set_emotion_and_gender_to_received_data(p_data, filename)

    files = load_files(p_data)
    raw_data_to_csv(files=files, path=p_data, keep_raw_data=keep_raw_data)

    if fig:
        p_plots = '{}\\plots'.format(path)
        p = Path(p_plots)
        p.mkdir(exist_ok=True)

        df = get_data(p_data)
        plot_data(df, fig_location=p_plots)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='session')

    parser.add_argument('-p', help='change path to program',
                        default=os.getcwd())
    parser.add_argument('-k', help='if set, keep raw data (txt files)',
                        action='store_true', default=False)
    parser.add_argument('--plot', help='if set, plot data',
                        action='store_true', default=False)


    args = vars(parser.parse_args())

    session(path=args['p'], keep_raw_data=args['k'],
            fig=args['plot'])
