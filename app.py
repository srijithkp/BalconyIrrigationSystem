from watering import cntrlValve,getCurrValveState
from flask import Flask, request
from flask import render_template
   
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/Watering/")
def watering():
    valveState = getCurrValveState()
    #print(valveState)
    return render_template('watering.html', **valveState)

@app.route("/Watering/<valve>/")
def action(valve):
    cntrlValve(valve)
    valveState = getCurrValveState()
    #print(valveState)
    return render_template('watering.html', **valveState)

@app.route('/Sensors/')
def sensors():
    return render_template('sensors.html')

@app.route('/Weather/')
def weather():
    return render_template('weather.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
