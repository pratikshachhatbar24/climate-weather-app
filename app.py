from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import requests
from datetime import datetime
import os

app = Flask(__name__)

# ============================================
# Load ML Model
# ============================================
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')

with open(os.path.join(MODEL_PATH, 'weather_model.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.join(MODEL_PATH, 'scaler.pkl'), 'rb') as f:
    scaler = pickle.load(f)

# ============================================
# OpenWeatherMap API Key
# ============================================
API_KEY = "9866c0221d47d52d56c3b798f99f5f61"  

# ============================================
# Weather Code to Icon Mapping
# ============================================
WEATHER_ICONS = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '❄️',
    'Mist': '🌫️',
    'Haze': '🌫️',
    'Fog': '🌫️',
    'Smoke': '🌫️'
}


# ============================================
# ROUTES
# ============================================
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/current-weather', methods=['POST'])
def current_weather():
    """Get current weather from OpenWeatherMap"""
    city = request.form.get('city', 'Mumbai')
    
    try:
        # Current Weather API
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if data.get('cod') != 200:
            return jsonify({'error': f"City '{city}' not found!", 'status': 'failed'})
        
        weather_main = data['weather'][0]['main']
        icon = WEATHER_ICONS.get(weather_main, '🌤️')
        
        result = {
            'status': 'success',
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp'], 1),
            'feels_like': round(data['main']['feels_like'], 1),
            'temp_min': round(data['main']['temp_min'], 1),
            'temp_max': round(data['main']['temp_max'], 1),
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # m/s to km/h
            'visibility': round(data.get('visibility', 10000) / 1000, 1),
            'clouds': data['clouds']['all'],
            'weather': data['weather'][0]['description'].title(),
            'weather_main': weather_main,
            'icon': icon,
            'icon_url': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
            'lat': data['coord']['lat'],
            'lon': data['coord']['lon']
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'})


@app.route('/forecast', methods=['POST'])
def forecast():
    """Get 5-day forecast from OpenWeatherMap"""
    city = request.form.get('city', 'Mumbai')
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if data.get('cod') != '200':
            return jsonify({'error': 'City not found!', 'status': 'failed'})
        
        # Get daily forecast (every 24h)
        forecasts = []
        seen_dates = set()
        
        for item in data['list']:
            date = item['dt_txt'].split(' ')[0]
            if date not in seen_dates and len(forecasts) < 5:
                seen_dates.add(date)
                weather_main = item['weather'][0]['main']
                forecasts.append({
                    'date': date,
                    'day': datetime.strptime(date, '%Y-%m-%d').strftime('%A'),
                    'temp': round(item['main']['temp'], 1),
                    'temp_min': round(item['main']['temp_min'], 1),
                    'temp_max': round(item['main']['temp_max'], 1),
                    'humidity': item['main']['humidity'],
                    'weather': item['weather'][0]['description'].title(),
                    'icon': WEATHER_ICONS.get(weather_main, '🌤️'),
                    'icon_url': f"http://openweathermap.org/img/wn/{item['weather'][0]['icon']}@2x.png",
                    'wind_speed': round(item['wind']['speed'] * 3.6, 1)
                })
        
        return jsonify({
            'status': 'success',
            'city': data['city']['name'],
            'forecasts': forecasts
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'})


@app.route('/air-quality', methods=['POST'])
def air_quality():
    """Get air quality data"""
    lat = request.form.get('lat', '19.07')
    lon = request.form.get('lon', '72.87')
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        aqi_labels = {1: 'Good 😊', 2: 'Fair 🙂', 3: 'Moderate 😐', 
                      4: 'Poor 😷', 5: 'Very Poor 🤢'}
        
        aqi = data['list'][0]['main']['aqi']
        components = data['list'][0]['components']
        
        result = {
            'status': 'success',
            'aqi': aqi,
            'aqi_label': aqi_labels.get(aqi, 'Unknown'),
            'co': round(components.get('co', 0), 2),
            'no2': round(components.get('no2', 0), 2),
            'o3': round(components.get('o3', 0), 2),
            'so2': round(components.get('so2', 0), 2),
            'pm2_5': round(components.get('pm2_5', 0), 2),
            'pm10': round(components.get('pm10', 0), 2)
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'})


@app.route('/predict', methods=['POST'])
def predict():
    """ML Model Temperature Prediction"""
    try:
        humidity = float(request.form['humidity'])
        pressure = float(request.form['pressure'])
        wind_speed = float(request.form['wind_speed'])
        co2_level = float(request.form['co2_level'])
        rainfall = float(request.form.get('rainfall', 0))
        cloud_cover = float(request.form.get('cloud_cover', 50))
        month = int(request.form['month'])
        day = int(request.form['day'])
        year = int(request.form['year'])
        
        from datetime import date
        day_of_year = date(year, month, day).timetuple().tm_yday
        
        features = np.array([[humidity, pressure, wind_speed,
                              co2_level, rainfall, cloud_cover,
                              month, day, year, day_of_year]])
        
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        
        return jsonify({
            'status': 'success',
            'prediction': round(prediction, 2),
            'unit': '°C'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'})


@app.route('/climate-trends')
def climate_trends():
    """Return climate trend data"""
    import pandas as pd
    
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'climate_data.csv')
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    yearly = df.groupby(df['Date'].dt.year).agg({
        'Temperature': 'mean',
        'CO2_Level': 'mean',
        'Humidity': 'mean',
        'Rainfall': 'sum'
    }).reset_index()
    
    monthly = df.groupby(df['Date'].dt.month).agg({
        'Temperature': 'mean'
    }).reset_index()
    
    return jsonify({
        'yearly': {
            'years': yearly['Date'].tolist(),
            'temperatures': yearly['Temperature'].round(2).tolist(),
            'co2_levels': yearly['CO2_Level'].round(2).tolist(),
            'humidity': yearly['Humidity'].round(2).tolist(),
            'rainfall': yearly['Rainfall'].round(2).tolist()
        },
        'monthly': {
            'months': ['Jan','Feb','Mar','Apr','May','Jun',
                       'Jul','Aug','Sep','Oct','Nov','Dec'],
            'temperatures': monthly['Temperature'].round(2).tolist()
        }
    })


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🌍 Climate Weather App Starting...")
    print("📡 API: OpenWeatherMap")
    print("🤖 ML Model: Loaded")
    print("🌐 URL: http://127.0.0.1:5000")
    print("=" * 50 + "\n")
    app.run(debug=True, port=5000)
