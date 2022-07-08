#!/usr/bin/python
# -*- coding:utf-8 -*-
from machine import UART,Pin,Timer
import time

led = Pin(25, Pin.OUT)
LED_state = True

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
        print("Set can config, LED Flashing 2HZ")
        # cfg pin = 0
        self.Cfg.value(1) #hardward set
        # self.uart.write("+++") #SOFT SET
        time.sleep(0.1) # must have
        
#         print("AT")
#         self.uart.write("AT\r")
#         self.uart.readline()
#         rxD = self.uart.readline()
#         print(rxD.decode('utf-8'))
        
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
        print(rxD.decode('utf-8'))
        
        time.sleep(0.1)
        self.Cfg.value(0)
        self.CAN_Reset()
        time.sleep(0.1)

# Define CAN variable
can = E810_TTL_CAN()

# Turing on LED to show activity
print("=== Starting PowerUp")
led.value(LED_state)

# Set CAN properties
print("=== Set CAN settings")
can.CAN_SetCAN()

# Do nothing at the Beginning
print("=== Waiting for 10s")
time.sleep(10)

# Send correct CAN message
print("=== Sending CAN message")
can.CAN_Send = '20 7F FF 00 FF 00 D0 06'

# Turn off LED to show finishing
print("=== Turn Off")
led.value(False)



