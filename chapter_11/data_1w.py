#!/usr/bin/python3
''' data_1w.py '''
import time
from w1thermsensor import W1ThermSensor

DATANAME = ["0:Temperature"]

class Device:
    ''' One-Wire DS18B20 device class '''
    def __init__(self):
        self.device = W1ThermSensor()
        self.name = DATANAME

    def get_name(self):
        ''' Return channel names '''
        return self.name

    def get_new(self):
        ''' Get new data set from device '''
        data = []
        data.append(self.device.get_temperature())
        return data

def main():
    ''' Main test '''
    onewire = Device()
    print(str(onewire.get_name()))
    for i in range(10):
        data_values = onewire.get_new()
        print(str(data_values))
        time.sleep(1)

if __name__ == '__main__':
    main()
#End
