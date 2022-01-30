# importing flask, render_template, requests and json
import requests
from flask import Flask, render_template, request, json, redirect, url_for

# Create an object named app
app = Flask(__name__)

# Create name and lastname variables for the fonction
name = "Enes"
lastname = "Turan"


# Create name and lastname variables for main page
@app.route('/', methods=['GET', 'POST'])
def home():
    # return render_template('main.html', name='Enes', lastname='Turan')
    return f'{name} {lastname}'


@app.route('/temperature', methods=['GET', 'POST'])
def temperature():
    return render_template('temperature.html')


@app.route('/temperature/<string:city>', methods=['GET', 'POST'])
def city(city):
    return f'{city}'

    # return render_template('temperature_city.html', city=city)


# Add a statement to run the Flask application which can be reached from any host on port 80
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
