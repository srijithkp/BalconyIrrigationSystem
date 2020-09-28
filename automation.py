import configparser
import logging
##### Variables ####
automationData = {}

try:
    config = configparser.ConfigParser()
    config.read('config.ini')
except configparser.MissingSectionHeaderError:
    raise WrongIniFormatError()


def automation_main():
    pass


def resetAvgDurationValues():
    logging.basicConfig(filename='activitiy.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Executed action to reset the average values')
    config.read('config.ini')
    for valve in config.options('WATERING_DURATION_AVG'):
        config.set('WATERING_DURATION_AVG', valve,str(0))
    with open('config.ini', 'w') as configfile:  # save
        config.write(configfile)


def updtManualDurationValues(manualValues):
    logging.basicConfig(filename='activitiy.log', level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Executed action to update the manual values')
    config.read('config.ini')
    #print(manualValues)
    for valve in config.options('WATERING_DURATION_MANUAL'):
        #print(f'{valve} : {manualValues[valve]}')
        config.set('WATERING_DURATION_MANUAL', valve, manualValues[valve])
    with open('config.ini', 'w') as configfile:  # save
        config.write(configfile)
    pass


def getAutomationData():
    config.read('config.ini')
    for valve in config.options('WATERING_DURATION_AVG'):
        automationData[valve+'avg'] = config.getint('WATERING_DURATION_AVG', valve)
    for valve in config.options('WATERING_DURATION_MANUAL'):
        automationData[valve] = config.getint('WATERING_DURATION_MANUAL', valve)

    #print(f'automationData:{automationData}')
    return automationData

def automation_main():
    try:
        pass
    except KeyboardInterrupt:
        pass
        # GPIO.cleanup()


if __name__ == "__main__":
    autowater()
