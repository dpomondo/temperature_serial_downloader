#!./bin/python

import argparse
import pandas as pd
from matplotlib import pyplot as plt
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
        # df_hist = df.hist(column=" temp1")

        # fig, axs = plt.subplots(2)
        fig, axs = plt.subplot_mosaic("AA;BC")
        # ax1 = fig.add_subplot()
        for doy, grp in days:
            axs["A"].plot(grp.index, grp, marker='+')
            grp.index -= grp.index.floor('D')
            axs["B"].plot(grp.index, grp)
            # axs["C"].hist(df, bins=20)
        axs["C"].plot(days_min)
        axs["C"].plot(days_max)

        fig.suptitle(f"{filename}")
        # plt.ylabel("Temp in C")
        # plt.xlabel("datetime")
        axs["A"].set_ylabel("Temp in C")
        axs["A"].set_xlabel("datetime")
        axs["B"].set_title("Day-on-Day Comparison")
        axs["B"].set_ylabel("Temp in C")
        axs["B"].set_xlabel("hour")
        axs["C"].set_ylabel("Temp in C")
        axs["C"].set_xlabel("Day of Year")
        axs["C"].legend(["Min", "Max"], loc="best")
        # plt.title(f"{filename}")
        axs["A"].grid(color='blue', linestyle='--')
        axs["B"].grid(color='blue', linestyle='--')
        axs["C"].grid(color='lightseagreen', linestyle='-')
        plt.show()


if __name__ == '__main__':
    # temp_filename = make_filename()
    args = parser.parse_args()

    try:
        make_chart(args.filename)
    except FileNotFoundError:
        print("Bad filename supplied")
