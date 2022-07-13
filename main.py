#!/usr/bin/python
# -*- coding:utf-8 -*-
from machine import UART,Pin,Timer
import time

led = Pin(25, Pin.OUT)

class E810_TTL_CAN(object):
    def __init__(self, CFG_PIN=2, RESET_PIN=3):
        self.uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
        
        # Reset and Cfg set 0
        self.Cfg = Pin(CFG_PIN,Pin.OUT)
        self.Reset = Pin(RESET_PIN,Pin.OUT)        
        self.Cfg.value(0) #set Transparent transmission mode
        self.CAN_Reset()
        
    def CAN_Reset(self):
        self.Reset.value(1) # reset
        self.Reset.value(0) 
    
    def CAN_Send(self, txData):
        self.uart.write(txData)
    
    def CAN_Revice(self):
        #rxData = bytes()
        #while  self.uart.any()>0 && self.uart.read(1)!='':
        rxData = self.uart.read(1)
        #print(rxData.decode('utf-8'))
        return rxData
    
    def CAN_SetCAN(self):
        # cfg pin = 0
        self.Cfg.value(1) #hardward set
        # self.uart.write("+++") #SOFT SET
        time.sleep(0.1) # must have
        
        #AT+CAN=<baud,id,mode><CR>
        #baud： CAN baud: kbps(6，10，20，50，100，120，125，150，200，250，400，500，600，750，1000)
        #id： Send frame ID (identifier)
        #mode2 mode： NDTF -> sends standard data frames
        #             EDTF -> sends extended data frame
        #AT+CAN=100,0,NDTF <CR>
        print("AT+CAN")
        self.uart.write("AT+CAN=125,0x1A9,NDTF\r")
        #self.uart.write("AT+CAN=100,0,NDTF\r")
        #self.uart.readline()
        rxD = self.uart.readline()
        
        time.sleep(0.1)
        self.Cfg.value(0)
        self.CAN_Reset()
        time.sleep(0.1)

# Delare CAN class
can = E810_TTL_CAN()

# Turing on LED to show activity
print("=== Starting PowerUp [LED ON]")
led.value(True)

# Set CAN properties
print("=== Set CAN")
can.CAN_SetCAN()

# Do nothing at the Beginning
print("=== Waiting for 10s")
time.sleep(10)

# Read message
read = ''
while not read:
    print("=== Wait for Message [LED BLINK FAST]")
    read = can.CAN_Revice()
    led.toggle()
    time.sleep(0.5)

# Check if read is empty
print("=== Read Message 0x1A9: " + read[7] + " " + read[6] + " " + read[5] + " " + read[4] + " " + read[3] + " " + read[2] + " " + read[1] + " " + read[0])

# Send correct CAN message
# Example IN  '20 7F FF 00 FF 00 50 06'
# Example OUT '20 7F FF 00 FF 00 D0 06'
read[6] = read[6] | 128 # Set bit 7 of Byte 6
can.CAN_Send(read[0] | (read[1] << 8) | (read[2] << 16) | (read[3] << 24) | (read[4] << 32) | (read[5] << 40) | (read[6] << 48) | (read[7] << 56))
print("=== Sent Message 0x1A9: " + read)

# Turn off LED to show finishing
print("=== Standby [LED BLINK SLOW])")
while true:
    led.toggle()
    time.sleep(2)