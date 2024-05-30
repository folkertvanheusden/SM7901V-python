#! /usr/bin/python3

# written by Folkert van Heusden.

# requires python3-pyserial and python3-paho-mqtt

import paho.mqtt.publish as publish
import serial
import statistics
import time

start = time.time()

readings = []

while True:
    rmsg = []

    # /dev/ttyS0 is the serial port on a raspberry pi
    # default for the sensor is 38400
    with serial.Serial('/dev/ttyS0', 115200, timeout = 1) as ser:
        try:
            msg = bytes([ 0x01, 0x03, 0x00, 0x00, 0x00, 0x01, 0x84, 0x0a ])
            ser.write(msg)

            while True:
                while len(rmsg) >= 7:
                    del rmsg[0]

                rmsg.append(int.from_bytes(ser.read(), 'big'))

                if len(rmsg) == 7 and rmsg[0] == 0x01 and rmsg[1] == 0x03 and rmsg[2] == 0x02:
                    break

            readings.append(((rmsg[3] << 8) | rmsg[4]) / 10)

        except Exception as e:
            print(e)
            time.sleep(0.5)

    now = time.time()

    # collect statistics every 5 seconds
    # that's around 1000 samples
    if now - start >= 5.0:
        start = now

        min_ = min(readings)
        avg_ = statistics.mean(readings)
        med_ = statistics.median(readings)
        max_ = max(readings)

        # you may want to change these
        publish.single('noise-levels/min', f'{min_}', hostname='192.168.64.1')
        publish.single('noise-levels/max', f'{max_}', hostname='192.168.64.1')
        publish.single('noise-levels/med', f'{med_}', hostname='192.168.64.1')
        publish.single('noise-levels/avg', f'{avg_}', hostname='192.168.64.1')

        print(now, min_, avg_, med_, max_, len(readings))

        readings = []
