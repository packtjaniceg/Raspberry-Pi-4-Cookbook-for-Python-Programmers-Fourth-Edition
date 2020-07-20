#!/usr/bin/env python3
''' xlo_borg3_part1.py '''
import time
import struct
import busio
from adafruit_bus_device.i2c_device import I2CDevice

CMPSADR = 0x0E
CTRL_REG1 = 0x10
CTRL_REG2 = 0x11
I2C_SDA_BCM = 2 #GPIO.BOARD Pin 3
I2C_SCL_BCM = 3 #GPIO.BOARD Pin 5

class Compass:
    ''' Compass class '''
    def __init__(self, addr=CMPSADR):
        ''' Constructor '''
        self.bus = busio.I2C(scl=I2C_SCL_BCM, sda=I2C_SDA_BCM)
        self.i2c = I2CDevice(self.bus, addr)
        self.init_compass()

    def write(self, data):
        ''' Write value to device '''
        with self.i2c as device:
            device.write(bytes(data))

    def read(self):
        ''' Read value from device '''
        with self.i2c as device:
            buffer = bytearray(1)
            device.readinto(buffer)
        return int.from_bytes(buffer, byteorder='big')

    def read_block_data(self, register, length):
        ''' Read block data from I2C device '''
        mag_data = bytearray(length)
        with self.i2c as device:
            device.readinto(mag_data, start=register, end=register+length)
        return mag_data

    def init_compass(self):
        ''' Initialise compass '''
        # Acquisition mode
        register = CTRL_REG2 # CTRL_REG2
        data  = (1 << 7)  # Reset before each acquisition
        data |= (1 << 5)  # Raw mode, do not apply user offsets
        data |= (0 << 5)  # Disable reset cycle
        self.write([register, data])
        # System operation
        register = CTRL_REG1 # CTRL_REG1
        data  = (0 << 5)  # Output data rate
                          # (10 Hz when paired with 128 oversample)
        data |= (3 << 3)  # Oversample of 128
        data |= (0 << 2)  # Disable fast read
        data |= (0 << 1)  # Continuous measurement
        data |= (1 << 0)  # Active mode
        self.write([register, data])

    def read_compass_raw(self):
        ''' Read raw compass value '''
        #x, y, z = readCompassRaw()
        self.write([0x00])
        [status, xh, xl, yh, yl,
         zh, zl, who, sm, oxh, oxl,
         oyh, oyl, ozh, ozl,
         temp, c1, c2] = self.read_block_data(0, 18)
        # Convert from unsigned to correctly signed values
        read_bytes = struct.pack('BBBBBB', xl, xh, yl, yh, zl, zh)
        x, y, z = struct.unpack('hhh', read_bytes)
        return x, y, z

if __name__ == '__main__':
    MY_COMPASS = Compass()
    try:
        while True:
            # Read the MAG Data
            MX, MY, MZ = MY_COMPASS.read_compass_raw()
            print("mX = %+06d, mY = %+06d, mZ = %+06d" % (MX, MY, MZ))
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Finished")
#End
