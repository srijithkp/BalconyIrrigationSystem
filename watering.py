#! /usr/bin/python3
##### Imports #####
import RPi.GPIO as GPIO
import datetime
import time

gpioDeviceMap = {
    'LeftOne'   : {'pin' : 33, 'state' : 'OFF'},
    'LeftTwo'   : {'pin' : 37, 'state' : 'OFF'},
    'LeftThree' : {'pin' : 36, 'state' : 'OFF'},
    'LeftFour'  : {'pin' : 32, 'state' : 'OFF'},
    'RightOne'  : {'pin' : 10, 'state' : 'OFF'},
    'RightTwo'  : {'pin' : 7, 'state' : 'OFF'},
    'RightThree': {'pin' : 5, 'state' : 'OFF'},
    'RightFour' : {'pin' : 16, 'state' : 'OFF'},
    'CentreTop' : {'pin' : 12, 'state' : 'OFF'},    
    'Pump'      : {'pin' : 3, 'state' : 'OFF'},
    'Fountain'  : {'pin' : 31, 'state' : 'OFF'},    
   }
deviceStateMap = {}
relayOn = False

GPIO.setmode(GPIO.BOARD)
for device in gpioDeviceMap:
    GPIO.setup(gpioDeviceMap[device]['pin'], GPIO.OUT, initial=GPIO.HIGH)

def gpio_toggle(device):
    gpio_read()
    if gpioDeviceMap[device]['state'] == 'OFF':
        print('Switching the '+device+' ON')
        #Switch ON The Pump
        if gpioDeviceMap['Pump']['state'] == 'OFF':
                GPIO.output(gpioDeviceMap['Pump']['pin'], GPIO.LOW)
        # Open the Relay
        GPIO.output(gpioDeviceMap[device]['pin'], GPIO.LOW)
    elif gpioDeviceMap[device]['state'] == 'ON':
        print('Switching the '+device+' OFF')
        # Close the Relay
        GPIO.output(gpioDeviceMap[device]['pin'], GPIO.HIGH)
        #Switch Off the Pump if no relays are Open
        if getRelayTotalStatus() == False:
            GPIO.output(gpioDeviceMap['Pump']['pin'], GPIO.HIGH)

def gpio_read():
    for device in gpioDeviceMap:
        if GPIO.LOW == GPIO.input(gpioDeviceMap[device]['pin']):
            gpioDeviceMap[device]['state']='ON'
        else:
            gpioDeviceMap[device]['state']='OFF'
        
        deviceStateMap[device] = gpioDeviceMap[device]['state']
    return deviceStateMap

def getRelayTotalStatus():
    relayOn = False
    for device in gpioDeviceMap:
        if device != 'Pump':
            if GPIO.LOW == GPIO.input(gpioDeviceMap[device]['pin']):
                relayOn = True
    return relayOn

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
