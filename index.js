const express = require('express')
const cors = require('cors')
const bodyParser = require('body-parser');
const axios = require('axios');
const kelvinToCelsius = require('kelvin-to-celsius');


// API base URL
const BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

//  API key
const API_KEY = "99fd063b248c10d275944af7307bc5a6"


const SendWeatherRequest = async (city) => {
    var clientServerOptions = {
        uri: BASE_URL + "q=" + city + "&appid=" + API_KEY,
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }
    try {
        const resp = await axios.get(clientServerOptions.uri, {
            headers: clientServerOptions.headers
        });
        return resp.data;
    } catch (err) {
        // Handle Error Here
        console.error(err);
    }
};

// Create express app
const app = express()
const port = 3456
app.use(cors())
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(bodyParser.raw());


app.get('/', (req, res) => {
    var response = {
        fistname: 'Enes',
        lastname: 'Turan'
    }
    res.json(response)
})


app.get('/temperature', async (req, res, next) => {
    try {
        const cityname = req.query.city;
        const weatherData = await SendWeatherRequest(cityname)
        let rawTempData = weatherData.main.temp;
        // Convert Kelvin to Celsius
        let celsiusData = kelvinToCelsius(rawTempData);
        let coords = weatherData.coord;
        var response = {
            temperature: celsiusData,
            // city: cityname,
            // coords: coords
        }
        res.status(200).json(response);
    } catch (error) {
        res.status(404).json(error);
        next(error)
    }
})

app.listen(port, () => {
    console.log(`Best Cloud Academy Case Study App listening at http://localhost:${port}`)
})
