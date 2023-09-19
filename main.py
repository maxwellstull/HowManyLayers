import requests
import json
import datetime
from classes import Hour, Forecast, FuzzyRecallDict





cur_lat = 41.946468
cur_long = -87.647328

params = {"latitude":cur_lat,
          "longitude":cur_long,
          "timezone":"auto",
          "forecast_days":2,
          "hourly":"temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,cloudcover,windspeed_10m,uv_index"}

url = "https://api.open-meteo.com/v1/forecast?"
x = requests.get(url, params=params)
#print(x.url)
print("API Call Returned")
ata = x.json()
#print(ata)
with open("test.json", "w" ) as fp:
    json.dump(ata, fp)


forecasty = Forecast(ata)

now = datetime.datetime.now()
print(repr(now))
rightnow = forecasty.getHour(now)
print(rightnow)