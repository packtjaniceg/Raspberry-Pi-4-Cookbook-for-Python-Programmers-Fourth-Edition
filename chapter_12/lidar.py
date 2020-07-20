#!/usr/bin/python3
''' lidar.py '''
import time
import busio
import adafruit_vl53l0x

I2C_SDA_BCM = 2 #GPIO.BOARD Pin 3
I2C_SCL_BCM = 3 #GPIO.BOARD Pin 5

I2C = busio.I2C(I2C_SCL_BCM, I2C_SDA_BCM)
SENSOR = adafruit_vl53l0x.VL53L0X(I2C)
SENSOR.measurement_timing_budget = 200000
while True:
    print(f'Range: {SENSOR.range}mm')
    time.sleep(2)
#End
