#!/usr/bin/python
# -*- coding:utf-8 -*-
from machine import UART,Pin,Timer
from rp2 import *
import time

# Define LED-Pin
led = Pin(25, Pin.OUT)

# LED ON
led.value(True)

# In-work indicator to false
inwork = True

# Loop counter
loop = 1

# Waiting for vehicle to poperly boot
print("=== Wait for 30s")
time.sleep(30)

# Filter IDs
id_filter_state = {0: CANID(0x227).get_id_filter()}
id_filter_toggle = {0: CANID(0x1A9).get_id_filter()}

# Repeat work until StSt is off
while inwork:

    # Initialize CAN controller for reading StSt state
    print("=== Initializing CAN")
    c = CAN(profile=CAN.BITRATE_125K_75,id_filters=id_filter_state)
    time.sleep(2)

    # Read payload
    frames = c.recv()
    payload_state = frames[0].get_data()

    # Output payload
    print("=== StSt State frame 227")
    print(payload_state)

    # Check for Bit2 in Byte3
    a = payload_state
    b = b'\x00\x00\x00\x04\x00\x00\x00\x00'
    a = (int.from_bytes(a, 'big') & int.from_bytes(b, 'big')).to_bytes(max(len(a), len(b)), 'big')
    n = b'\x00\x00\x00\x00\x00\x00\x00\x00'

    # If Bit 2 of Byte 3 is set = StSt OFF
    if a != n:

        print("=== StSt is now OFF")
        inwork = False

    else:

        # Initialize CAN controller for reading StSt toggle
        c = CAN(profile=CAN.BITRATE_125K_75,id_filters=id_filter_toggle)
        time.sleep(2)

        # Read payload
        frames = c.recv()
        payload = frames[0].get_data()

        # Output payload
        print("=== StSt State frame 227")
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

    print("Loop:")
    print(loop)
    print("==============================")
    loop += 1

while True:

    # Go to infinite Standby
    print("=== Standby [LED BLINK SLOW])")

    led.toggle()
    time.slaeep(2)
