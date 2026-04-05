import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Generate 5 years of daily data
start_date = datetime(2019, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(365 * 5)]

data = []
for date in dates:
    month = date.month
    day_of_year = date.timetuple().tm_yday
    
    # Realistic seasonal temperature pattern
    base_temp = 25 + 10 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
    temp = base_temp + np.random.normal(0, 3)
    
    # Add warming trend (climate change)
    year_offset = (date.year - 2019) * 0.3
    temp += year_offset
    
    humidity = max(20, min(100, 60 + 20 * np.sin(2 * np.pi * day_of_year / 365) + np.random.normal(0, 10)))
    pressure = max(990, min(1040, 1013 + np.random.normal(0, 5)))
    wind_speed = max(0, 15 + np.random.normal(0, 8))
    rainfall = max(0, np.random.exponential(2) if month in [6,7,8,9] else np.random.exponential(0.5))
    co2 = 410 + (date.year - 2019) * 2.5 + np.random.normal(0, 1)
    visibility = max(1, min(10, 7 + np.random.normal(0, 2)))
    cloud_cover = max(0, min(100, 50 + np.random.normal(0, 25)))
    
    data.append({
        'Date': date.strftime('%Y-%m-%d'),
        'Temperature': round(temp, 2),
        'Humidity': round(humidity, 2),
        'Pressure': round(pressure, 2),
        'Wind_Speed': round(wind_speed, 2),
        'Rainfall': round(rainfall, 2),
        'CO2_Level': round(co2, 2),
        'Visibility': round(visibility, 2),
        'Cloud_Cover': round(cloud_cover, 2)
    })

df = pd.DataFrame(data)
df.to_csv('climate_data.csv', index=False)
print(f"✅ Dataset created: {df.shape}")
print(df.head())
print(f"\n{df.describe()}")