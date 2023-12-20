import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

api_key = '99bfb66b2a786503cd7248953b728b5d'
api_base_url = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    if not city:
        return jsonify({'error': 'City name is required'})

    params = {
        'q': city,
        'appid': api_key,
        'units': 'imperial'  # You can change this to 'imperial' for Fahrenheit
    }

    try:
        response = requests.get(api_base_url, params=params)

        print("API Request URL:", response.url)  # Add this line for debugging
        print("API Response:", response.text)    # Add this line for debugging

        response.raise_for_status()
        weather_data = response.json()

        if weather_data['cod'] == '404':
            return jsonify({'error': 'City not found'})

        weather_info = {
            'city': weather_data['name'],
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'icon': weather_data['weather'][0]['icon'],
        }
        weather_info['temperature'] = round((weather_info['temperature'] * 9 / 5) + 32, 2)

        return jsonify(weather_info)

    except requests.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
