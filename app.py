from watering import gpio_toggle,gpio_read
from flask import Flask, request
from flask import render_template
   
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/invalid/')
def invalid():
    return render_template('invalid.html')

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

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
