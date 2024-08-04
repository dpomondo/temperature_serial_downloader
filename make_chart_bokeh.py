#!./bin/python

from time import strftime, localtime
import argparse
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot, column
from bokeh.models import HoverTool
from bokeh.models import DatetimeTickFormatter
from bokeh.models.tickers import DatetimeTicker, DaysTicker
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
        df = pd.read_csv(f, parse_dates=True, index_col='datetime', dtype={
                         " temp1": np.float64},
                         na_values=" ",
                         )
        y_axis_min = int(df.min().values[0]) - 1
        y_axis_max = int(df.max().values[0]) + 1
        # temp_xaxis = list(df.index)
        days = df.groupby(lambda ts: ts.dayofyear)
        days_min = df.groupby(lambda ts: ts.dayofyear).min()
        days_max = df.groupby(lambda ts: ts.dayofyear).max()
        days_median = df.groupby(lambda ts: ts.dayofyear).median()
        # df_hist = df.hist(column=" temp1")

        temp_chart_tooltips = [("day", "@x"),
                               ("temp", "@y")]
        # hover_tool.formatters = {"@x": "datetime"}
        # temp_chrt = figure(title="Daily Temps", sizing_mode="stretch_width")
        temp_chrt = figure(title="Daily Temps",
                           width=1200, height=275,
                           y_range=(y_axis_min, y_axis_max),
                           toolbar_location=None,
                           tools=[HoverTool(
                               formatters={"$x": "datetime"}
                           )],
                           tooltips=temp_chart_tooltips,
                           x_axis_type="datetime",
                           )
        days_chrt = figure(title="Day-on-Day",
                           y_range=(y_axis_min, y_axis_max),
                           toolbar_location=None,
                           tools=[HoverTool()],
                           tooltips=[("day", "$index"), ("temp", "@y")],
                           x_axis_type="datetime",
                           )
        min_max_chrt = figure(title="Mid, Max, Median",
                              y_range=(y_axis_min, y_axis_max),
                              toolbar_location=None,
                              )

        for doy, grp in days:
            temp_chrt.line(grp.index, grp)
            grp.index -= grp.index.floor('D')
            days_chrt.line(grp.index, grp)
        min_max_chrt.line(days_min.index, days_min)
        min_max_chrt.line(days_max.index, days_max)
        min_max_chrt.line(days_median.index, days_median)

        tick_num = len(days)
        print(f"tick_num: {tick_num}")
        temp_chrt.xaxis.ticker = DatetimeTicker(desired_num_ticks=tick_num)
        # temp_chrt.xaxis.ticker = DaysTicker(days=[df.index], desired_num_ticks=tick_num)
        temp_chrt.yaxis.ticker.desired_num_ticks = y_axis_max - y_axis_min
        temp_chrt.xgrid.grid_line_color = "indigo"
        temp_chrt.xgrid.grid_line_alpha = 0.4
        temp_chrt.ygrid.grid_line_color = "indigo"
        temp_chrt.ygrid.grid_line_alpha = 0.4
        temp_chrt.xgrid.grid_line_dash = [3, 4]
        temp_chrt.ygrid.grid_line_dash = [3, 4]
        temp_chrt.yaxis.ticker.num_minor_ticks = 4

        # days_chrt.xaxis.formatter.context = DatetimeTickFormatter(
        #     # context_which="all",
        #     context="None",
        #     # days="%H",
        #     )
        # days_chrt.toolbar.autohide = True
        # min_max_chrt.toolbar.autohide = True
        grid = gridplot([[days_chrt, min_max_chrt]],
                        width=600, height=275
                        )
        # grid = row(days_chrt, min_max_chrt)
        # return grid
        grid.toolbar_location = None
        combined = column(temp_chrt, grid)
        return combined


if __name__ == '__main__':
    args = parser.parse_args()
    try:
        chart = make_chart(args.filename)
        show(chart)
    except FileNotFoundError:
        print("Bad filename supplied")
