#! /usr/bin/python3
##### Imports #####
import RPi.GPIO as GPIO
import configparser

######### Common #########
GPIO.setmode(GPIO.BOARD)


try:
    config = configparser.ConfigParser()
    config.read('config.ini')
except configparser.MissingSectionHeaderError:
    raise WrongIniFormatError()

######## Variables #######
valveState = {}
valvePinMap = {}
for valve in config.options('VALVE_PIN_MAP'):
    valvePinMap[valve] = config.getint('VALVE_PIN_MAP',valve)
    valveState[valve] = 'OFF'
    GPIO.setup(valvePinMap[valve], GPIO.OUT, initial=GPIO.HIGH)

####Function to control the valve #####
def cntrlValve(valve):
    getCurrValveState()
    if valveState[valve] == 'OFF':
        print('Switching the '+valve+' ON')
        # Open the Relay
        GPIO.output(valvePinMap[valve], GPIO.LOW)
        valveState[valve] = 'ON'
        #Switch ON The Pump
        if valveState['pump'] == 'OFF':
                GPIO.output(valvePinMap['pump'], GPIO.LOW)
                valveState['pump'] = 'ON'
    elif valveState[valve] == 'ON':
        print('Switching the '+valve+' OFF')
        GPIO.output(valvePinMap[valve], GPIO.HIGH)
        valveState[valve] = 'OFF'
        # Close the Relay
        #Switch Off the Pump if no relays are Open
        for valve,state in valveState.items():
            if valve == 'pump':
                #Finished checking all valves and none are open; Turn off the pump
                GPIO.output(valvePinMap['pump'], GPIO.HIGH)
                valveState['pump'] = 'OFF'
            else:
                if state == 'ON':
                    break

def getCurrValveState():
    return valveState

def gpio_cleanup():
    pass
    GPIO.cleanup()

def getLastWatered():
    try:
		pass
    except:
        return "NEVER!"

def autowater():
    try:
        pass
    except KeyboardInterrupt:
        pass
        GPIO.cleanup()

if __name__ == "__main__":
    autowater()
