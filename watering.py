#! /usr/bin/python3
##### Imports #####
import RPi.GPIO as GPIO
import datetime
import time

gpioDeviceMap = {
    'Pump'      : {'pin' : 7, 'state' : 'OFF'},
    'PlantOne'  : {'pin' : 11, 'state' : 'OFF'},
    'PlantTwo'  : {'pin' : 13, 'state' : 'OFF'},
    'PlantThree': {'pin' : 15, 'state' : 'OFF'},   
    'PlantFour' : {'pin' : 29, 'state' : 'OFF'},
    'PlantFive' : {'pin' : 31, 'state' : 'OFF'},   
    'PlantSix'  : {'pin' : 33, 'state' : 'OFF'},
    'PlantSeven': {'pin' : 35, 'state' : 'OFF'},
    'PlantEight': {'pin' : 37, 'state' : 'OFF'}
   }
deviceStateMap = {}

GPIO.setmode(GPIO.BOARD)
for device in gpioDeviceMap:
    GPIO.setup(gpioDeviceMap[device]['pin'], GPIO.OUT, initial=GPIO.HIGH)

def gpio_toggle(device):
    if gpioDeviceMap[device]['state'] == 'OFF':
        print('Switching the '+device+' ON')
        GPIO.output(gpioDeviceMap['Pump']['pin'], GPIO.LOW)
        # Open the Relay
        GPIO.output(gpioDeviceMap[device]['pin'], GPIO.LOW)
    elif gpioDeviceMap[device]['state'] == 'ON':
        print('Switching the '+device+' OFF')
        GPIO.output(gpioDeviceMap['Pump']['pin'], GPIO.HIGH)
        # Close the Relay<
        GPIO.output(gpioDeviceMap[device]['pin'], GPIO.HIGH)

def gpio_read():
    for device in gpioDeviceMap:
        gpioState = GPIO.input(gpioDeviceMap[device]['pin'])
        
        if gpioState == GPIO.LOW:
            gpioDeviceMap[device]['state']='ON'
        else:
             gpioDeviceMap[device]['state']='OFF'
        deviceStateMap[device] = gpioDeviceMap[device]['state']
    return deviceStateMap

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
