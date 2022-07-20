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
print("=== Initializing CAN")
# profile 2: 125 kBaud
# Only use ID 1A9
c = CAN(profile=CAN.BITRATE_125K_75,id_filters=id_filter)

# Switch between vehicle and offline testing
if True: # True for vehicle, False for offline testing
    
    # Wait for 30s
    print("=== Wait for 30s")
    time.sleep(30)
    
    # Read frame
    frames = c.recv() # For Vehicle
    payload = frames[0].get_data() # For Vehicle
    
else:
    
    # Wait for 2s --> Faster Testing
    print("=== Wait for 2s (TESTING)")
    time.sleep(2)
    payload = b'\x20\x7F\xFF\x00\xFF\x00\x50\x00'

# Output payload
print("=== Read payload from CAN")
print(payload)

# Set Bit 7 on Byte 6
a = payload
b = b'\x00\x00\x00\x00\x00\x00\x80\x00'
payload = (int.from_bytes(a, 'big') | int.from_bytes(b, 'big')).to_bytes(max(len(a), len(b)), 'big')

# Notify
print("=== New payload for Sending")
print(payload)

# Define CANFrame
f = CANFrame(CANID(0x1A9), data=payload)

# Send Frame
c.send_frame(f)
print("=== Sent message")

# Go to infinite Standby
print("=== Standby [LED BLINK SLOW])")
while True:
    led.toggle()
    time.sleep(2)
