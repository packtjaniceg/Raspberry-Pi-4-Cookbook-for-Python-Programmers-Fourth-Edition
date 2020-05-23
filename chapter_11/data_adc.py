#!/usr/bin/python3
''' data_adc.py '''
import time
import busio
from adafruit_bus_device.i2c_device import I2CDevice

LIGHT = 0; TEMP = 1; EXT = 2; POT = 3
ADC_CH = [LIGHT, TEMP, EXT, POT]
ADC_ADR = 0x48
ADC_CYCLE = 0x04
BUS_GAP = 0.25
DATANAME = ["0_Light", "1_Temperature",
            "2_External", "3_Potentiometer"]
I2C_SDA_BCM = 2 #GPIO.BOARD Pin 3
I2C_SCL_BCM = 3 #GPIO.BOARD Pin 5

class Device:
    ''' I2C ADC device class '''
    def __init__(self, addr=ADC_ADR):
        ''' Class constructor '''
        self.name = DATANAME
        self.bus = busio.I2C(scl=I2C_SCL_BCM, sda=I2C_SDA_BCM)
        self.i2c = I2CDevice(self.bus, addr)
        # Flush power up value
        self.read()
        self.read()
        time.sleep(BUS_GAP)
        # Set cycle mode
        with self.i2c as device:
            device.write(bytes([ADC_CYCLE]))
        time.sleep(BUS_GAP)
        self.read()

    def get_name(self):
        ''' Return channel names '''
        return self.name

    def read(self):
        ''' Read value from device '''
        with self.i2c as device:
            buffer = bytearray(1)
            device.readinto(buffer)
        return int.from_bytes(buffer, byteorder='big')

    def get_new(self):
        ''' Get new data set from device '''
        data = []
        for ch in ADC_CH:
            time.sleep(BUS_GAP)
            data.append(self.read())
        return data

def main():
    ''' Main test '''
    adc = Device()
    print(str(adc.get_name()))
    for i in range(10):
        data_values = adc.get_new()
        print(str(data_values))
        time.sleep(1)

if __name__ == '__main__':
    main()
#End
