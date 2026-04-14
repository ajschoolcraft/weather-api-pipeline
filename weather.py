import os
import time
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["WEATHER_API_KEY"]

api_url = "https://api.weatherapi.com/v1/forecast.json"

zip_codes = [
    "90045",  # Los Angeles, CA
    "10001",  # New York, NY
    "60601",  # Chicago, IL
    "98101",  # Seattle, WA
    "33101",  # Miami, FL
    "77002",  # Houston, TX
    "85001",  # Phoenix, AZ
    "19103",  # Philadelphia, PA
    "78205",  # San Antonio, TX
    "92101",  # San Diego, CA
    "75201",  # Dallas, TX
    "95113",  # San Jose, CA
    "78701",  # Austin, TX
    "32801",  # Orlando, FL
    "80202",  # Denver, CO
    "02108",  # Boston, MA
    "97201",  # Portland, OR
    "89101",  # Las Vegas, NV
    "37201",  # Nashville, TN
    "30303",  # Atlanta, GA
]

results = []

for zip_code in zip_codes:
    params = {"key": API_KEY, "q": zip_code, "days": 7}
    response = requests.get(api_url, params=params)
    data = response.json()

    for day in data["forecast"]["forecastday"]:
        results.append(
            {
                "zip_code": zip_code,
                "city": data["location"]["name"],
                "region": data["location"]["region"],
                "date": day["date"],
                "max_temp_f": day["day"]["maxtemp_f"],
                "min_temp_f": day["day"]["mintemp_f"],
                "condition": day["day"]["condition"]["text"],
            }
        )

    time.sleep(1)

df = pd.DataFrame(results)
print(df)
print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")

df.to_csv("weather_data.csv", index=False)
