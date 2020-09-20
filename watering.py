#! /usr/bin/python3
##### Imports #####
import RPi.GPIO as GPIO
import configparser
import datetime

######### Common #########
GPIO.setmode(GPIO.BOARD)
AVG_TIME_UPDATE_THRESHOLD = 5 #seconds

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
    valvePinMap[valve] = config.getint('VALVE_PIN_MAP',valve)
    valveState[valve] = 'OFF'
    valveOnTime[valve] = datetime.datetime.now()
    valveOnDuration[valve] = 0
    valveOnCount[valve] = 0
    GPIO.setup(valvePinMap[valve], GPIO.OUT, initial=GPIO.HIGH)

####Function to control the valve #####
def cntrlValve(valve):
    getCurrValveState()
    if valveState[valve] == 'OFF':
        print('Switching the '+valve+' ON')
        # Open the Relay

        GPIO.output(valvePinMap[valve], GPIO.LOW)
        valveState[valve] = 'ON'
        valveOnTime[valve] = datetime.datetime.now()
        #print(valveOnTime[valve])
        #Switch ON The Pump
        if valveState['pump'] == 'OFF':
                GPIO.output(valvePinMap['pump'], GPIO.LOW)
                valveState['pump'] = 'ON'
    elif valveState[valve] == 'ON':
        print('Switching the '+valve+' OFF')
        GPIO.output(valvePinMap[valve], GPIO.HIGH)
        valveState[valve] = 'OFF'
        #Save average duration for automation
        saveAverageDuration(valve)
        #Switch Off the Pump if no relays are Open
        checkPump(valve)

def getCurrValveState():
    return valveState

def saveAverageDuration(valve):
    valveOnDuration[valve] = datetime.datetime.now() - valveOnTime[valve]
    valveOnCount[valve] +=1

    if valveOnDuration[valve].seconds > AVG_TIME_UPDATE_THRESHOLD:
        config.read('config.ini')
        valveOnTimeCurrAv = config.getfloat('WATERING_DURATION_AVG',valve)
        print(f'valveOnTimeCurrAv:{valveOnTimeCurrAv}')
        valveOnTimeNewAv = valveOnTimeCurrAv + ((valveOnDuration[valve].seconds - valveOnTimeCurrAv)/valveOnCount[valve])
        print(f'valveOnTimeCurrAv:{valveOnTimeCurrAv},valveOnTimeNewAv:{round(valveOnTimeNewAv)}')
        config.set('WATERING_DURATION_AVG',valve, str(round(valveOnTimeNewAv)))
        with open('config.ini', 'w') as configfile: #save
            config.write(configfile)

def checkPump(valve):
    for valve,state in valveState.items():
        if valve == 'pump':
            #Finished checking all valves and none are open; Turn off the pump
            GPIO.output(valvePinMap['pump'], GPIO.HIGH)
            valveState['pump'] = 'OFF'
        else:
            if state == 'ON':
                break

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
