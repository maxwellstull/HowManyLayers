import requests
import json
import datetime
from classes import Hour, Forecast, FuzzyRecallDict, Recommender, CtoF
import pandas as pd




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

print(forecasty.getHour(current_time))


when = datetime.datetime(2023, 10, 12, 13, 0, 0)
if when < current_time:
    when = current_time
duration = 3

print(forecasty.getRelevantHours(when, duration))

data = pd.DataFrame(forecasty.getLRList(when))
data['Activity'] = [1]
print(data)
rec = Recommender()
rec.train()
rec.LRPredict(data)
