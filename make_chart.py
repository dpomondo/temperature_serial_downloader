#!./bin/python

import argparse
import pandas as pd
from matplotlib import pyplot as plt


def make_filename():
    from datetime import date
    month = date.today().strftime('%B')
    return f"{month}_temperatures.csv"


temp_filename = make_filename()
parser = argparse.ArgumentParser(description="make a chart from a csv file")
parser.add_argument('filename',
                    default=temp_filename,
                    nargs='?',
                    help='(Optional) Name of file from which to make a chart')


def make_chart(filename):
    with open(filename, 'r') as f:
        df = pd.read_csv(f, parse_dates=True, index_col='datetime')
        df.plot(marker='+')

        plt.show()


if __name__ == '__main__':
    # temp_filename = make_filename()
    args = parser.parse_args()

    try:
        make_chart(args.filename)
    except FileNotFoundError:
        print("Bad filename supplied")
