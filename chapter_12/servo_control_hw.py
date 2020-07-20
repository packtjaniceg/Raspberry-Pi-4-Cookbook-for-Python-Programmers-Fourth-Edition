#!/usr/bin/env python3
''' servo_control_hw.py

 HARDWARE SETUP
 GPIO
 2[==X==========]26[=======]40
 1[VDC==========]25[=======]39
 V=3.3V X=Gnd
 D=SDA C=SCL
'''
import time
import busio
from adafruit_bus_device.i2c_device import I2CDevice

#PWM Registers
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06
LED0_ON_H = 0x07
LED0_OFF_L = 0x08
LED0_OFF_H = 0x09

BUS_GAP = 0.25
PWMHZ = 50
PWMADR = 0x40
I2C_SDA_BCM = 2 #GPIO.BOARD Pin 3
I2C_SCL_BCM = 3 #GPIO.BOARD Pin 5


class Servo:
    ''' Hardware PCA9685 based servo control '''
    def __init__(self, pwm_freq=PWMHZ, addr=PWMADR):
        ''' Constructor '''
        self.bus = busio.I2C(scl=I2C_SCL_BCM, sda=I2C_SDA_BCM)
        self.i2c = I2CDevice(self.bus, addr)
        self.pwm_init(pwm_freq)

    def read(self):
        ''' Read value from device '''
        with self.i2c as device:
            buffer = bytearray(1)
            device.readinto(buffer)
        return int.from_bytes(buffer, byteorder='big')

    def write(self, data):
        ''' Write value to device '''
        with self.i2c as device:
            device.write(bytes(data))

    def pwm_init(self, pwm_freq):
        ''' Initalise the PWM controller '''
        prescale = 25000000.0 / 4096.0   # 25MHz / 12-bit
        prescale /= float(pwm_freq)
        prescale = prescale - 0.5 #-1 then +0.5 to round to
                                  # nearest value
        prescale = int(prescale)
        self.write([MODE1, 0x00]) #RESET
        mode = self.read()
        self.write([MODE1, (mode & 0x7F)|0x10]) #SLEEP
        self.write([PRESCALE, prescale])
        self.write([MODE1, mode]) #restore mode
        time.sleep(0.005)
        self.write([MODE1, mode|0x80]) #restart

    def set_pwm(self, channel, on, off):
        ''' Set PWM value '''
        on = int(on)
        off = int(off)
        self.write([LED0_ON_L+4*channel, on & 0xFF])
        self.write([LED0_ON_H+4*channel, on>>8])
        self.write([LED0_OFF_L+4*channel, off & 0xFF])
        self.write([LED0_OFF_H+4*channel, off>>8])

def main():
    ''' Main test function '''
    servo_min = 205  # Min pulse 1ms 204.8 (50Hz)
    servo_max = 410  # Max pulse 2ms 409.6 (50Hz)
    my_servo = Servo()
    my_servo.set_pwm(0, 0, servo_min)
    time.sleep(2)
    my_servo.set_pwm(0, 0, servo_max)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Finish")
#End
