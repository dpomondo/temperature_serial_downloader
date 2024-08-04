#!./bin/python

import time
import serial
import csv
from utilities import make_filename


def return_list():
    with serial.Serial('/dev/ttyACM0', 115200, timeout=2) as ser:
        print("Dialogue open with serial port!\n")
        # ser.open()
        ser.write(b'x')
        time.sleep(1)
        ser.write(b'v')
        time.sleep(1)
        # ser.flush()
        index = 0
        while True:
            index += 1
            line = ser.readline().decode('utf-8')
            print(f"serial port sent:\t{line}")
            if 'CSV' in line or 'START' in line:
                break
            if index >= 15:
                print("Never received a `CSV START` message")
                break

        ser.write(b'c')
        print("Trying to get CSV data!")
        index = 0
        results = []
        while True:
            line = ser.readline().decode('utf-8')
            print(f"received {index}:\t{line}")
            if "CSV" not in line:
                results.append(line)
            index += 1
            if index >= 600:
                print("hit max replies(600)")
                break
            if "END" in line:
                print("serial port sent `END` command")
                break
    return results


def process_results(csv_raw_list):
    processed_results = []
    reader = csv.reader(csv_raw_list, delimiter=',')
    for row in reader:
        # if "CSV" not in row:
        if row[0] not in ["CSV", "datetime"]:
            datetime = row[0]
            temp = row[1]
            processed_results.append([datetime, temp])
    return processed_results


# def make_filename():
#     from datetime import date
#     month = date.today().strftime('%b_%Y')
#     return f"{month}_temperatures.csv"


def write_results(csv_processed_list):
    times = []
    filename = make_filename()
    print(f"Writing results to {filename}")
    # with open('temperatures.csv', 'r') as t:
    try:
        with open(filename, 'r') as t:
            reader = csv.DictReader(t)
            for row in reader:
                times.append(row['datetime'])
    except FileNotFoundError:
        print(f"File not found, creating file {filename}")
        with open(filename, 'a') as t:
            writer = csv.writer(t, delimiter=',')
            writer.writerow(["datetime", " temp1"])
    # with open('temperatures.csv', 'a') as t:
    with open(filename, 'a') as t:
        writer = csv.writer(t, delimiter=',')
        for row in csv_processed_list:
            timestamp = row[0]
            # temp = str(row[2])
            temp = row[1]
            if timestamp not in times:
                writer.writerow([timestamp, temp])


if __name__ == "__main__":
    csv_list = return_list()
    csv_list_better = process_results(csv_list)
    write_results(csv_list_better)
    # for row in csv_list_better:
    #     print(row, len(row))
