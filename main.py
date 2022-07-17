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
        rxData = bytes()
        #while self.uart.any()>0 && self.uart.read(1)!='':
        rxData = self.uart.read()
        #print(rxData.decode('utf-8'))
        print(rxData)
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
        print("set AT+CAN + Protocol- Mode")
        self.uart.write('AT+MODE=PROTOL\r')
        self.uart.write("AT+CAN=125,0,NDTF\r")
        
        time.sleep(0.1)
        self.Cfg.value(0)
        self.CAN_Reset()
        time.sleep(0.1)
        
    def Return(self):
        print("")
        print("[Return]")
        print(can.uart.readline())
        print(can.uart.readline())
        print("")


# Delare CAN class
can = E810_TTL_CAN()

# Show return values
can.Return()

# Turing on LED to show activity
print("=== Starting PowerUp [LED ON]")
led.value(True)

# Set CAN properties
print("=== Set CAN")
can.CAN_SetCAN()

# Show return values
can.Return()

print("=== Waiting for 20s")
time.sleep(20)
led.toggle()

# Send Message in Protocol mode
can.CAN_Send(b'\x08\x00\x00\x01\xA9\x20\x7F\xFF\x00\xFF\x00\xD0\x00')

# Show return values
can.Return()

# Go to infinite Standby
print("=== Standby [LED BLINK SLOW])")
while True:
    led.toggle()
    time.sleep(2)