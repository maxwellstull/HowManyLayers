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
          "daily":"sunrise,sunset",
          "hourly":"temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,cloudcover,windspeed_10m,uv_index,rain,snowfall,precipitation_probability"}

url = "https://api.open-meteo.com/v1/forecast?"
x = requests.get(url, params=params)
print("API Call Returned")
APIReturn = x.json()
with open("test.json", "w" ) as fp:
    json.dump(APIReturn, fp)

forecasty = Forecast(APIReturn)

current_time = datetime.datetime.now()

when = datetime.datetime(2023, 10, 12, 13, 0, 0)
if when < current_time:
    when = current_time
duration = 3

rightnow = forecasty.getRelevantHours(when, duration)
print(rightnow)

rec = Recommender()
rec.feed_hourly_info(rightnow)

rec.train()

res = rec.get_recommendation()
print(res)
