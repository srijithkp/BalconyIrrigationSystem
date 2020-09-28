from watering import cntrlValve, getCurrValveState, runAutomatedWatering
from automation import getAutomationData, resetAvgDurationValues, updtManualDurationValues
from flask import Flask, request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/Watering/")
def watering():
    valveState = getCurrValveState()
    # print(valveState)
    return render_template('watering.html', **valveState)


@app.route("/Watering/<valve>/")
def action(valve):
    cntrlValve(valve)
    valveState = getCurrValveState()
    # print(valveState)
    return render_template('watering.html', **valveState)


@app.route('/Automation/')
def automation():
    automationData = getAutomationData()
    return render_template('automation.html', **automationData)


@app.route('/Automation/AutomationResetAvg/')
def automationResetAvg():
    resetAvgDurationValues()
    automationData = getAutomationData()
    return render_template('automation.html', **automationData)


@app.route('/Automation/AutomationRunAvg/')
def automationRunAvg():
    runAutomatedWatering('Average')
    automationData = getAutomationData()
    return render_template('automation.html', **automationData)


@app.route('/Automation/AutomationUpdtManual/')
def automationUpdtManual():
    manualValues = request.args.to_dict()
    updtManualDurationValues(manualValues)
    automationData = getAutomationData()
    return render_template('automation.html', **automationData)


@app.route('/Automation/AutomationRunManual/')
def automationRunManual():
    runAutomatedWatering('Manual')
    automationData = getAutomationData()
    return render_template('automation.html', **automationData)


@app.route('/Sensors/')
def sensors():
    return render_template('sensors.html')


@app.route('/Weather/')
def weather():
    return render_template('weather.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
