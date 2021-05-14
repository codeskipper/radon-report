#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    radon-report.py

    Calculate and report radon statistics from measurements
    Works with exported raw data in csv format from Airthings Wave sensors
    Follows Norwegian guidelines as described in https://dsa.no/radon/slik-maler-du-radon#
'''

import os
import sys
#from pathlib import Path
import logging
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams


def main():
    try:
        args = sys.argv[1:]
        ifile = args[0]
    except IndexError:
        print('Please specify the input file as argument')
        sys.exit(-1)

    try:
        # Read the CSV into a pandas data frame (df)
        #   With a df you can do many things
        #   most important: visualize data with Seaborn
        df = pd.read_csv(ifile, delimiter=';')
        ifile_name = os.path.basename(ifile)
    except FileNotFoundError:
        print('Could not find input file %s' % ifile)
        sys.exit(-1)
    except Exception as ex:
        logging.exception('caught an error')
        sys.exit(-1)
    df['recorded'] = pd.to_datetime(df['recorded'])
    print('\n')
    print('Radon report for file: ', ifile_name)
    print('First observations in file:')
    print(df.head(1))
    print('\n')
    print('Last observations in file:')
    print(df.tail(1))
    print('\n')
    delta_dates = max(df['recorded']) - min(df['recorded'])
    print('Difference between first and last record in file: ', delta_dates)
    seconds = delta_dates.total_seconds()
    interval_secs = seconds / len(df.index)
    print('Observation interval: %3.3f seconds' % interval_secs)
    print('Calculating 7-day rolling average')
    df_window = round(7 * 24 * 3600 / interval_secs)
    print('observation window size: %d' % df_window)
    df['RADON_7_day_moving_avg  Bq/m3'] = df.rolling(window=df_window)['RADON_SHORT_TERM_AVG Bq/m3'].mean()
    print('Last observations in file with 7-day-average added:')
    print(df.tail(1))

    print('\n')
    print('Calculating yearly Radon average as prescribed in https://dsa.no/radon/slik-maler-du-radon#')
    # select period for calculation, one year is best if available
    if delta_dates.days >= 365:
        # Use one-year period ending in last record
        start_date = max(df['recorded']) - pd.Timedelta(365, unit='D')
        df = df[(df['recorded'] > start_date)]
        corr_factor = 1
        print('Using ', start_date, ' as start, and Yearly Mean Correction Factor: ', corr_factor)
    else: # use winter period (November 1 to April 1) must be at least two months
        # ToDo: determine largest portion of data in winter period and use for selection, bail out if less than two months
        df = df[(df['recorded'] > "2020-11-01") & (df['recorded'] < "2021-04-01")]
        print('Winter period (November 1 - April 1) selected for yearly mean calculation, Yearly Mean Correction Factor: 0.75')
        corr_factor = 0.75
    #df.info()
    print('First row selected:')
    print(df.head(1))
    print('\n')
    print('Last row selected:')
    print(df.tail(1))
    print('\n')
    delta_dates = max(df['recorded']) - min(df['recorded'])
    print('Number of days selected: %d' % delta_dates.days)
    radon_mean = df['RADON_SHORT_TERM_AVG Bq/m3'].mean()
    print('Radon mean: %4.3f Bq/㎥' % radon_mean)
    radon_y_mean = radon_mean * corr_factor
    if not corr_factor == 1:
        print('Factor for yearly mean: %1.3f' % corr_factor)
        print('Calculated yearly mean: %4.3f Bq/㎥' % radon_y_mean)

    # add the yearly average as a column for plotting
    df['radon_y_mean Bq/m3'] = radon_y_mean
    print('\n')

    # now to plot the 7-day avg
    plt.style.use('ggplot')
    rcParams['font.family'] = 'DejaVu Sans'
    ax = plt.gca()

    #df.plot(x='recorded', y=['RADON_SHORT_TERM_AVG Bq/m3', 'RADON_7_day_moving_avg  Bq/m3', 'radon_y_mean'])
    df.plot(x='recorded', y=['RADON_7_day_moving_avg  Bq/m3', 'radon_y_mean Bq/m3'], ax=ax)

    # how our axes should look
    ax.set_xlabel('Date')
    ax.set_ylabel('Radon (Bq/m3)')        # ToDo: figure out how to support the font glyph for '㎥'
    ax.set_title('Radon plot for: %s' % ifile_name)
    ax.grid(True)
    #ax.legend(loc='upper left');

    # save the plot to image file
    image_file = os.path.splitext(ifile)[0] + ' - Radon-rapport plot.png'
    print('Saving plot til image file', image_file)
    try:
        plt.savefig(image_file)
    except:
        print('Error saving plot to image file')

    plt.show()



if __name__ == '__main__':
    main()
