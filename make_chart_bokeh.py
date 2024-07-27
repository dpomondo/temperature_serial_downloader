#!./bin/python

import argparse
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot, row
# from matplotlib import pyplot as plt
from utilities import make_filename


# def make_filename():
#     from datetime import date
#     month = date.today().strftime('%b_%Y')
#     return f"{month}_temperatures.csv"


# temp_filename = make_filename()
parser = argparse.ArgumentParser(description="make a chart from a csv file")
parser.add_argument('filename',
                    default=make_filename(),
                    # default=temp_filename,
                    nargs='?',
                    help='(Optional) Name of file from which to make a chart')


# partly stolen from:
# https://stackoverflow.com/questions/68997190/typeerror-float-argument-must-be-a-string-or-a-number-not-datetime-time-in
def make_chart(filename):
    with open(filename, 'r') as f:
        df = pd.read_csv(f, parse_dates=True, index_col='datetime')
        days = df.groupby(lambda ts: ts.dayofyear)
        days_min = df.groupby(lambda ts: ts.dayofyear).min()
        days_max = df.groupby(lambda ts: ts.dayofyear).max()
        days_median = df.groupby(lambda ts: ts.dayofyear).median()
        # df_hist = df.hist(column=" temp1")

        # temp = figure(title="Daily Temps", sizing_mode="stretch_width")
        temp = figure(title="Daily Temps")
        days_ch = figure(title="Day-on-Day")
        min_max = figure(title="Mid, Max, Median")

        for doy, grp in days:
            temp.line(grp.index, grp)
            grp.index -= grp.index.floor('D')
            days_ch.line(grp.index, grp)
        min_max.line(days_min.index, days_min)
        min_max.line(days_max.index, days_max)
        min_max.line(days_median.index, days_median)

        grid = gridplot([[temp], [days_ch, min_max]],
                        sizing_mode="stretch_width")
        # grid = row(days_ch, min_max)
        return grid


if __name__ == '__main__':
    # temp_filename = make_filename()
    args = parser.parse_args()

    try:
        chart = make_chart(args.filename)
        # chart.show()
        show(chart)
    except FileNotFoundError:
        print("Bad filename supplied")
