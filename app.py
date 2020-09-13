from watering import gpio_toggle,gpio_read
from flask import Flask, request
from flask import render_template
   
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/Watering/")
def watering():
    stateDict = gpio_read()
    #print(stateDict)
    return render_template('watering.html', **stateDict)

@app.route("/Watering/<device>/")
def action(device):
    gpio_toggle(device)

    stateDict = gpio_read()
    #print(stateDict)
    return render_template('watering.html', **stateDict)

@app.route('/Sensors/')
def sensors():
    return render_template('sensors.html')

@app.route('/Weather/')
def weather():
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
