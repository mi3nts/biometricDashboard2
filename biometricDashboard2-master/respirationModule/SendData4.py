# CODE TO SEND PREVIOUSLY RECORDED EEG DATA VIA AN LSL DATA OUTLET

# CODE AUTHORED BY: SHAWHIN TALEBI

import time
import csv
from pylsl import StreamInfo, StreamOutlet

# initialize the info for an 82 element LSL outlet
# stream name = 'sampleData'
# stream data kind = 'All' (CGX M-128, CGX AIM2, Tobii Pro Glasses)
# channel_count = 155
# nominal_srate = 500 (sample rate)
# channel_format = 'float32'
# source_id = 'sampleSource'
info = StreamInfo("sampleData", "All", 82, 500, "float32", "sampleSource")

# create an outlet from the info
outlet = StreamOutlet(info)

# send data
print("now sending data...")
# open EEGsample.csv
with open("sampleDataBM.csv") as csvfile:
    # read the .csv file
    readCSV = csv.reader(csvfile, delimiter=",")

    # start forever while loop to stream data
    while True:
        # for every row of data in .csv file
        for row in readCSV:
            # if the row corresponds to the header move to next row
            if row[0] == "Fp1":
                continue
            # initialize a data list
            data = []
            # for every element in the row convert it from a string to a float
            # and store it in data
            for ele in row:
                data.append(float(ele))
            # send data using the LSL outlet
            outlet.push_sample(data)
            # wait 10 ms
            time.sleep(0.01)
