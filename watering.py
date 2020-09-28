#! /usr/bin/python3
##### Imports #####
import RPi.GPIO as GPIO
import configparser
import datetime
from automation import getAutomationData
from flask import render_template
import logging

######### Common #########
GPIO.setmode(GPIO.BOARD)
AVG_TIME_UPDATE_THRESHOLD = 15  # seconds
ON_TIME_MAX_THRESHOLD = 99  # seconds

try:
    config = configparser.ConfigParser()
    config.read('config.ini')
except configparser.MissingSectionHeaderError:
    raise WrongIniFormatError()

######## Variables #######
valveState = {}
valvePinMap = {}
valveOnTime = {}
valveOnDuration = {}
valveOnCount = {}
for valve in config.options('VALVE_PIN_MAP'):
    valvePinMap[valve] = config.getint('VALVE_PIN_MAP', valve)
    valveState[valve] = 'OFF'
    valveOnTime[valve] = datetime.datetime.now()
    valveOnDuration[valve] = 0
    valveOnCount[valve] = 0
    GPIO.setup(valvePinMap[valve], GPIO.OUT, initial=GPIO.HIGH)

####Function to control the valve #####
def cntrlValve(valve):
    getCurrValveState()
    if valveState[valve] == 'OFF':
        setValveOn(valve)
    elif valveState[valve] == 'ON':
        setValveOff(valve)

def setValveOn(valve):
    print('Switching the valve: ' + valve + ' to ON state')
    # Open the Relay
    GPIO.output(valvePinMap[valve], GPIO.LOW)
    valveState[valve] = 'ON'
    valveOnTime[valve] = datetime.datetime.now()
    logging.basicConfig(filename='activitiy.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Switching the %s to ON state', valve)
    # print(valveOnTime[valve])
    # Switch ON The Pump
    if valveState['pump'] == 'OFF':
		GPIO.output(valvePinMap['pump'], GPIO.LOW)
		valveState['pump'] = 'ON'

def setValveOff(valve):
    print('Switching the ' + valve + ' OFF')
    GPIO.output(valvePinMap[valve], GPIO.HIGH)
    valveState[valve] = 'OFF'
    valveOnDuration[valve] = datetime.datetime.now() - valveOnTime[valve]
    logging.basicConfig(filename='activitiy.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Switching the valve: %s to OFF state; On Duration: %s', valve, valveOnDuration[valve])
    # Save average duration for automation
    saveAverageDuration(valve)
    # Switch Off the Pump if no relays are Open
    checkPump(valve)

def getCurrValveState():
    return valveState


def saveAverageDuration(valve):
    valveOnCount[valve] +=1

    if valve != "pump" and valve != 'fountain':
        if valveOnDuration[valve].seconds > AVG_TIME_UPDATE_THRESHOLD:
            config.read('config.ini')
            valveOnTimeCurrAv = config.getint('WATERING_DURATION_AVG', valve)
            # print(f'valveOnTimeCurrAv:{valveOnTimeCurrAv}')
            valveOnTimeNewAv = valveOnTimeCurrAv + \
                ((valveOnDuration[valve].seconds -
                  valveOnTimeCurrAv) / valveOnCount[valve])
            # print(f'valveOnTimeCurrAv:{valveOnTimeCurrAv},valveOnTimeNewAv:{round(valveOnTimeNewAv)}')
            config.set('WATERING_DURATION_AVG', valve,
                       str(round(valveOnTimeNewAv)))
            with open('config.ini', 'w') as configfile:  # save
                config.write(configfile)


def checkPump(valve):
    for valve, state in valveState.items():
        if valve == 'pump':
            # Finished checking all valves and none are open; Turn off the pump
            GPIO.output(valvePinMap['pump'], GPIO.HIGH)
            valveState['pump'] = 'OFF'
        else:
            if state == 'ON':
                break


def runAutomatedWatering(type):
    valveConfigDuration = {}
    config.read('config.ini')
    if type == 'Average':
        logging.basicConfig(filename='activitiy.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info('Starting Automated watering with Average values')
        for valve in config.options('WATERING_DURATION_AVG'):
            valveConfigDuration[valve] = config.getint('WATERING_DURATION_AVG', valve)
    elif type == 'Manual':
        logging.basicConfig(filename='activitiy.log', level=logging.INFO, format='%(asctime)s %(message)s')
        logging.info('Starting Automated watering with Manual values')
        for valve in config.options('WATERING_DURATION_MANUAL'):
            valveConfigDuration[valve[:-3]] = config.getint('WATERING_DURATION_MANUAL', valve)

    #print(valveConfigDuration)
    for key in valveConfigDuration:
        valveCurrOnDuration = 0
        valveOnTime = datetime.datetime.now()
        setValveOn(key)
        while (valveCurrOnDuration < valveConfigDuration[key]):
            valveCurrOnDuration = (datetime.datetime.now() - valveOnTime).seconds
            #print(f'{key}: {valveCurrOnDuration}')
        else:
            setValveOff(key)
    #print(valveConfigDuration)

    # setValveOn()
    # setValveOff()

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
