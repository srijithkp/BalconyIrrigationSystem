#! /usr/bin/python3
##### Imports #####
import RPi.GPIO as GPIO
import datetime
import time

gpioDeviceMap = {'Pump':7,
                'plantOne': 11,
                'plantTwo': 13,
                'plantThree': 15,
                'plantFour': 29,
                'plantFive': 31,
                'plantSix': 33,
                'plantSeven': 35}

gpioDeviceState ={};

GPIO.setmode(GPIO.BOARD)
for device in gpioDeviceMap:
    GPIO.setup(gpioDeviceMap[device], GPIO.OUT, initial=GPIO.HIGH)

def gpio_ctrl(device, state):
    if state == 'on':
        print('Switching the Pump ON')
        GPIO.output(gpioDeviceMap['Pump'], GPIO.LOW)
        # Open the Relay
        GPIO.output(gpioDeviceMap[device], GPIO.LOW)
    elif state == 'off':
        # Switching the Pump OFF
        GPIO.output(gpioDeviceMap['Pump'], GPIO.HIGH)
        # Close the Relay<
        GPIO.output(gpioDeviceMap[device], GPIO.HIGH)

def gpio_read():
    #print(device)
    for device in gpioDeviceMap:
        gpioState = GPIO.input(gpioDeviceMap[device])
        
        if gpioState == GPIO.LOW:
             gpioDeviceState[device]='On'
        else:
             gpioDeviceState[device]='Off'
    
    return gpioDeviceState

def gpio_cleanup():
    GPIO.cleanup()

def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"

def autowater():
    try:
        pass
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    autowater()
