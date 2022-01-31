# importing flask, render_template, requests and json modules
import requests
import json
from flask import Flask, render_template, request, json, redirect, url_for

# Create an object named app
app = Flask(__name__)


# API base URL
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# City Name
CITY = "izmir"

# Your API key
API_KEY = "99fd063b248c10d275944af7307bc5a6"

# updating the URL
URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY

# Sending HTTP request
response = requests.get(URL)

# checking the status code of the request
if response.status_code == 200:

    # retrieving data in the json format
    data = response.json()

    # take the main dict block
    main = data['main']

    # getting temperature
    temperature = main['temp']

    # print(f"{CITY:-^35}")
    print(f"Temperature: {temperature}")
else:
    # showing the error message
    print("Error in the HTTP request")


# Create name and lastname json for main page
@app.route('/', methods=['GET', 'POST'])
def home():
    return '{"name":"Enes", "lastname":"Turan"}'


# Create a route for the API page
@app.route('/temperature', methods=['GET'])
def endpoint():
    CITY = request.args.get('city')
    URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
    weather_api_aldisi = requests.get(URL)
    if weather_api_aldisi.status_code == 200:
        veri = weather_api_aldisi.json()
        main = veri['main']
        sicaklik = main['temp']
        # Kelvin to Celsius conversion
        sicaklik = (sicaklik - 273.15)
    # Sıcaklık değeri virgül sonrası 2 basamaklı hale çevrildikten sonra string olarak döndürüldü
    return '{"temperature":' + str(round(sicaklik, 2)) + '}'


# Add a statement to run the Flask application which can be reached from any host on port 80
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
