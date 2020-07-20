#!/usr/bin/env python3
''' xlo_borg3.py '''
import time
import math
import struct
import busio
from adafruit_bus_device.i2c_device import I2CDevice

CMPSADR = 0x0E
CTRL_REG1 = 0x10
CTRL_REG2 = 0x11
I2C_SDA_BCM = 2 #GPIO.BOARD Pin 3
I2C_SCL_BCM = 3 #GPIO.BOARD Pin 5

CAL = 100 #take CAL samples
FILENAME = "mag.cal"
DEBUG = True

class Compass:
    ''' Compass class '''
    def __init__(self, addr=CMPSADR, new_cal=False):
        ''' Constructor '''
        self.bus = busio.I2C(scl=I2C_SCL_BCM, sda=I2C_SDA_BCM)
        self.i2c = I2CDevice(self.bus, addr)
        self.init_compass()
        self.offset, self.scaling = self.read_cal(new_cal)
        if DEBUG:
            print(f"offset:{str(self.offset)} scaling:{self.scaling}")

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

    def read_cal(self, new_cal=False, filename=FILENAME):
        ''' Read the calibration from file '''
        if not new_cal:
            try:
                with open(filename, 'r') as mag_cal_file:
                    line = mag_cal_file.readline()
                    offset = line.split()
                    line = mag_cal_file.readline()
                    scaling = line.split()
                    if not offset or not scaling:
                        raise ValueError()
                    else:
                        offset = list(map(float, offset))
                        scaling = list(map(float, scaling))
            except (OSError, IOError, TypeError, ValueError) as exp:
                print(f"No Cal Data: {exp}")
                new_cal = True
        if new_cal:
            print("Perform New Calibration")
            offset, scaling = self.calibrate_compass()
            self.write_cal(offset, scaling)
        return offset, scaling

    def write_cal(self, offset, scaling):
        ''' Write the calibration to file '''
        if DEBUG:
            print("Write Calibration")
            print(f"offset:{offset}")
            print(f"scaling:{scaling}")
        with open(FILENAME, 'w') as mag_cal_file:
            for value in offset:
                mag_cal_file.write(str(value)+" ")
            mag_cal_file.write("\n")
            for value in scaling:
                mag_cal_file.write(str(value)+" ")
            mag_cal_file.write("\n")

    def calibrate_compass(self, samples=CAL):
        ''' Perform calibration of the compass '''
        MAXS16 = 32768
        SCALE = 1000.0
        avg = [0, 0, 0]
        min_value = [MAXS16, MAXS16, MAXS16]
        max_value = [-MAXS16, -MAXS16, -MAXS16]
        print("Move sensor around axis (start in 5 sec)")
        time.sleep(5)
        for calibrate in range(samples):
            for idx, value in enumerate(self.read_compass_raw()):
                avg[idx] += value
                avg[idx] /= 2
                if value > max_value[idx]:
                    max_value[idx] = value
                if value < min_value[idx]:
                    min_value[idx] = value
            time.sleep(0.1)
            if DEBUG:
                print(f"#{calibrate:02} min=[{min_value[0]:+06},"
                      + f"{min_value[1]:+06},{min_value[2]:+06}]"
                      + f" avg[{int(avg[0]):+06},{int(avg[1]):+06},"
                      + f"{int(avg[2]):+06}] max=[{max_value[0]:+06},"
                      + f"{max_value[1]:+06},{max_value[2]:+06}]")
        offset = []
        scaling = []
        for idx, value in enumerate(min_value):
            mag_range = max_value[idx]-min_value[idx]
            offset.append((mag_range/2)+min_value[idx])
            scaling.append(SCALE/mag_range)
        return offset, scaling

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

    def read_compass(self):
        ''' Read a value from the compass '''
        raw = self.read_compass_raw()
        if DEBUG:
            print(f"mX = {raw[0]:+06}, mY = {raw[1]:+06}, "
                  + f"mZ = {raw[2]:+06}")

        read = []
        for idx, value in enumerate(raw):
            adj = value-self.offset[idx]
            read.append(adj*self.scaling[idx])
        return read

    def read_compass_angle(self, cal=True):
        ''' Read compass and covert into an angle '''
        if cal:
            read = self.read_compass()
        else:
            read = self.read_compass_raw()
        angle = math.atan2(read[1], read[0]) # cal angle in radians
        if angle < 0:
            angle += (2 * math.pi) # ensure positive
        angle = (angle*360)/(2*math.pi) #report in degrees
        return angle

if __name__ == '__main__':
    MY_COMPASS = Compass()
    try:
        while True:
            # Read the MAG Data
            MX, MY, MZ = MY_COMPASS.read_compass_raw()
            if not DEBUG:
                print(f"mX = {MX:+06}, mY = {MY:+06}, mZ = {MZ:+06}")
            print(f"Angle: {MY_COMPASS.read_compass_angle():3.2f}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Finished")
#End
