#!/usr/bin/python3
''' log_adc.py '''
import time
import datetime
import data_adc as dataDevice

DEBUG = True
FILE = True
SAMPLE_PERIOD = 10
DATA_LOG = "data.log"

def get_header(data_names):
    ''' Create formated data header '''
    header = f"{' ':6}\t{'Time':{len(timestamp(time.time()))}}"
    for name in data_names:
        header += f"\t{name}"
    return header

def get_body(counter, now, data_names, data_values):
    ''' Create formated data body '''
    time_str = timestamp(now)
    body = f"{counter:<6}\t{time_str:{len(time_str)}}"
    for i, name in enumerate(data_names):
        body += f"\t{data_values[i]:{len(name)}}"
    return body

def timestamp(now):
    ''' generate timestamp '''
    return datetime.datetime.fromtimestamp(now).strftime(
        '%Y-%m-%d %H:%M:%S')

if FILE:
    LOG_FILE = open(DATA_LOG, 'w')

def main():
    ''' main data log loop '''
    counter = 0
    my_data = dataDevice.Device()
    my_data_names = my_data.get_name()
    header = get_header(my_data_names)
    if DEBUG:
        print(header)
    if FILE:
        LOG_FILE.write(header+"\n")
    while True:
        now = time.time()
        data = my_data.get_new()
        counter += 1
        body = get_body(counter, now, my_data_names, data)
        if DEBUG:
            print(body)
        if FILE:
            LOG_FILE.write(body+"\n")
        while time.time() <= now+SAMPLE_PERIOD:
            time.sleep(0.1)

try:
    main()
finally:
    if FILE:
        LOG_FILE.close()
#End
