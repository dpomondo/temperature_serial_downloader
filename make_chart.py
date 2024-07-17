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


def make_chart(filename):
    with open(filename, 'r') as f:
        df = pd.read_csv(f, parse_dates=True, index_col='datetime')
        df.plot(marker='+')

        plt.ylabel("Temp in C")
        plt.xlabel("datetime")
        plt.title(f"{filename}")
        plt.grid(color='blue', linestyle='--')
        plt.show()


if __name__ == '__main__':
    # temp_filename = make_filename()
    args = parser.parse_args()

    try:
        make_chart(args.filename)
    except FileNotFoundError:
        print("Bad filename supplied")
