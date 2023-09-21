import requests
import json
import datetime
from classes import Hour, Forecast, FuzzyRecallDict, Recommender





cur_lat = 41.946468
cur_long = -87.647328

params = {"latitude":cur_lat,
          "longitude":cur_long,
          "timezone":"auto",
          "forecast_days":2,
          "hourly":"temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,cloudcover,windspeed_10m,uv_index"}

url = "https://api.open-meteo.com/v1/forecast?"
x = requests.get(url, params=params)
print("API Call Returned")
APIReturn = x.json()
with open("test.json", "w" ) as fp:
    json.dump(APIReturn, fp)

forecasty = Forecast(APIReturn)

current_time = datetime.datetime.now()

when = datetime.datetime(2023, 9, 21, 14, 0, 0)
duration = 3

rightnow = forecasty.getHour(when)
rightnow = forecasty.getRelevantHours(when, duration)
print(rightnow)
rec = Recommender()


