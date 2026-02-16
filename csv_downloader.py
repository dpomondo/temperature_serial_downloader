#!./bin/python
"""import serial data and save it in a csv format, assumes that we're talkingto
the correct device and the device will send the data in the correct format, as
so far no negotiations or error checking are implemented"""

import time
import csv
import argparse
from utilities import make_filename
import serial


DATA_DIR = "data"
serial_target = ["/dev/ttyACM0", "/dev/ttyUSB0", "/dev/ttyUSB1"]
parser = argparse.ArgumentParser(
    description="download csv data over serial port")
parser.add_argument(
    "port",
    choices=serial_target,
    default=serial_target[0],
    # default=temp_filename,
    nargs="?",
    help="(Optional) Serial Port with which to talk",
)
parser.add_argument(
    "-o",
    "--output",
    default=make_filename(data_dir=DATA_DIR),
    nargs="?",
    help="(Optional) File Destination",
)


def return_list(serial_port):
    with serial.Serial(serial_port, 115200, timeout=2) as ser:
        print(f"Dialogue open with {serial_port}\n")
        # ser.open()
        ser.write(b"x")
        time.sleep(1)
        ser.write(b"v")
        time.sleep(1)
        # ser.flush()
        index = 0
        while True:
            index += 1
            line = ser.readline().decode("utf-8")
            print(f"serial port sent:\t{line}")
            if "CSV" in line or "START" in line:
                break
            if index >= 15:
                print("Never received a `CSV START` message")
                break
                # should this raise an error? it just falls through, negating
                # the whole point

        # ser.write(b'c')
        # changed pico program, this should be the new way to trigger printing
        ser.write(b"p")
        print("Trying to get CSV data!")
        index = 0
        results = []
        while True:
            line = ser.readline().decode("utf-8")
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
    reader = csv.reader(csv_raw_list, delimiter=",")
    for row in reader:
        # if "CSV" not in row:
        if row[0] not in ["CSV", "datetime"]:
            datetime = row[0]
            temp = row[1]
            processed_results.append([datetime, temp])
    return processed_results


def write_results(csv_processed_list, output_file):
    times = []
    print(f"Writing results to {output_file}")
    try:
        with open(output_file, "r") as t:
            reader = csv.DictReader(t)
            for row in reader:
                times.append(row["datetime"])
    except FileNotFoundError:
        print(f"File not found, creating file {output_file}")
        with open(output_file, "a") as t:
            writer = csv.writer(t, delimiter=",")
            writer.writerow(["datetime", " temp1"])
    # with open('temperatures.csv', 'a') as t:
    total_lines, newlin, oldlin = 0, 0, 0
    with open(output_file, "a") as t:
        writer = csv.writer(t, delimiter=",")
        for row in csv_processed_list:
            total_lines += 1
            timestamp = row[0]
            # temp = str(row[2])
            temp = row[1]
            if timestamp not in times:
                newlin += 1
                writer.writerow([timestamp, temp])
            else:
                oldlin += 1
    print(
        f"Processed {total_lines} total lines, with {newlin} new and {oldlin} old lines"
    )


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        csv_list = return_list(args.port)
        csv_list_better = process_results(csv_list)
        write_results(csv_list_better, args.output)
    except Exception as e:
        print(f"Error:\n\t{e}\nbad serial port provided maybe?!?")
