import requests
import json
from classes import Hour, Forecast

cur_lat = 41.946468
cur_long = -87.647328

params = {"latitude":cur_lat,
          "longitude":cur_long,
          "hourly":"temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,cloudcover,windspeed_10m"}

url = "https://api.open-meteo.com/v1/forecast?"
x = requests.get(url, params=params)
#print(x.url)
ata = x.json()
#print(ata)
with open("test.json", "w" ) as fp:
    json.dump(ata, fp)

forecasty = Forecast(ata)