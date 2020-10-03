import requests
import configparser
import datetime

weatherData = {}


def getWeatherData():
    config = configparser.ConfigParser()
    config.read('config.ini')
    apiKey = config['openweathermap']['apikey']
    zipCode = config['openweathermap']['zipcode']
    countryCode = config['openweathermap']['countrycode']
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={},{}&units=metric&appid={}".format(zipCode,countryCode,apiKey)
    req = requests.get(api_url)
    data = req.json()
    weatherData['temp'] = "{0:.2f}".format(data["main"]["temp"])
    weatherData['feelsLike'] = "{0:.2f}".format(data["main"]["feels_like"])
    weatherData['weatherMain'] = data["weather"][0]["main"]
    weatherData['weatherId'] = data["weather"][0]["id"]
    weatherData['location'] = data["name"]
    weatherData['pressure'] = data["main"]["pressure"]
    weatherData['humidity'] = data["main"]["humidity"]
    weatherData['windspeed'] = data["wind"]["speed"]
    weatherData['sunrise'] = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    weatherData['sunset'] = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    return weatherData
