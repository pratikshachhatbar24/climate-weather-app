# climate-weather-app
This project is a climate and weather application designed to provide real-time and forecasted atmospheric data for locations worldwide. The app utilizes external weather APIs to deliver accurate and up-to-date information, helping users understand current environmental conditions and future trends.
# 🌦️ Climate Weather App with EDA, ML & Live API

## 📌 Project Overview
This project is a **Climate Weather Application** that integrates:

- 📊 Exploratory Data Analysis (EDA) on historical weather dataset  
- 🤖 Machine Learning (ML) model for weather prediction  
- 🌐 Real-time weather data using OpenWeather API  
- 💻 Live web application for user interaction  

The system analyzes past climate data and combines it with live API data to provide accurate and dynamic weather insights.

---

## 🚀 Features

### 📊 Exploratory Data Analysis (EDA)
- Data cleaning and preprocessing  
- Temperature, humidity, and pressure analysis  
- Correlation heatmaps and trend visualization  
- Seasonal and pattern analysis  

### 🤖 Machine Learning Model
- Trained on historical weather dataset  
- Predicts temperature / weather conditions  
- Model evaluation and performance metrics  

### 🌐 API Integration
- Integrated with **OpenWeather API**  
- Fetches real-time weather data  
- Dynamic weather updates based on user input  

### 💻 Live Web App
- User-friendly interface  
- Search weather by city  
- Displays real-time + predicted results  

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Data Analysis:** Pandas, NumPy  
- **Visualization:** Matplotlib, Seaborn  
- **Machine Learning:** Scikit-learn  
- **Web Framework:** Flask / Streamlit  
- **API Handling:** Requests  
- **Environment Management:** python-dotenv  

---

## 🔌 API Used

- **OpenWeatherMap API**
  - Provides real-time weather data
  - Includes:
    - Temperature  
    - Humidity  
    - Wind speed  
    - Weather conditions  

---

## 📂 Project Structure
climate-weather-app/
│
├── data/                      # 📊 Dataset files
│   ├── raw/                   # Original dataset
│   └── processed/             # Cleaned dataset
│
├── notebooks/                 # 📓 Jupyter notebooks for EDA
│   └── eda_analysis.ipynb
│
├── models/                    # 🤖 Saved ML models
│   └── model.pkl
│
├── src/                       # 🔧 Source code
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── predict.py
│   └── utils.py
│
├── app/                       # 🌐 Web application
│   ├── app.py                 # Main app (Flask / Streamlit)
│   ├── routes.py              # (if Flask)
│   ├── templates/             # HTML templates (Flask)
│   │   └── index.html
│   └── static/                # CSS / JS files
│
├── api/                       # 🌐 API integration
│   └── weather_api.py
│
├── config/                    # ⚙️ Config files
│   └── config.py
│
├── .env                       # 🔑 Environment variables (API key)
├── .gitignore                 # 🚫 Ignored files
├── requirements.txt           # 📦 Dependencies
├── README.md                  # 📘 Project documentation
└── run.py                     # ▶️ Entry point (optional)
