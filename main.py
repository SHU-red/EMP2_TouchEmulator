#!/usr/bin/python
# -*- coding:utf-8 -*-
from machine import UART,Pin,Timer
from rp2 import *
import time

# Define LED-Pin
led = Pin(25, Pin.OUT)

# LED ON
led.value(True)

# Filter IDs
id_filter = {0: CANID(0x1A9).get_id_filter()}

# Initialize CAN controller
# profile 2: 125 kBaud
# Only use ID 1A9
c = CAN(profile=CAN.BITRATE_125K_75,id_filters=id_filter)

# Wait for 20s
print("=== Wait for 20s")
time.sleep(20)

# Read frame
frames = c.recv()
payload = frames[0].get_data()

# Set Bit 7 on Byte 6
a = payload
b = b'\x00\x00\x00\x00\x00\x00\xD0\x00'
payload = (int.from_bytes(a, 'big') | int.from_bytes(b, 'big')).to_bytes(max(len(a), len(b)), 'big')

# Notify
print("Payload for sent message")
print(payload)

# Define CANFrame
f = CANFrame(CANID(0x1A9), data=payload)

# Send Frame
print("=== Sending CAN Frame")
c.send_frame(f)

# Go to infinite Standby
print("=== Standby [LED BLINK SLOW])")
while True:
    led.toggle()
    time.sleep(2)
