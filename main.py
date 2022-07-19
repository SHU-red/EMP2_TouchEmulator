#!/usr/bin/python
# -*- coding:utf-8 -*-
from machine import UART,Pin,Timer
from rp2 import *
import time

# Define LED-Pin
led = Pin(25, Pin.OUT)

# Initialize CAN controller
c = CAN(profile=BITRATE_125K_75,mode=NORMAL)

# Wait for 20s
print("=== Wait for 20s")
time.sleep(20)

# Define CANFrame
f = CANFrame(CANID(0x1A9), dlc=8, data=b'\x20\x7F\xFF\x00\xFF\x00\xD0\x00')

# Send Frame
print("=== Sending CAN Frame")
c.send_frame(f)

# Go to infinite Standby
print("=== Standby [LED BLINK SLOW])")
while True:
    led.toggle()
    time.sleep(2)
