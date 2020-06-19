from watering import gpio_ctrl,gpio_read
from flask import Flask
from flask import render_template
   
app = Flask(__name__)

@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('watering.html')

@app.route("/Watering/")
def watering():
    return render_template('watering.html')

@app.route("/Watering/<plantNumber>/<action>")
def action(plantNumber, action):
    gpio_ctrl(plantNumber,action)
    print(plantNumber)
    templateData = gpio_read()
    print(templateData)

    #if status == 0:
     #   templateData = {plantNumber:'On'}
        #print(templateData)
    #else:
     #   templateData = {plantNumber:'Off'}

    return render_template('watering.html', **templateData)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
