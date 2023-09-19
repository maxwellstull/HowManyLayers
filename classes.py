from datetime import datetime 
import pytz 

class Forecast():
    def __init__(self, json):
        # Location information
        self.latitude = json['latitude']
        self.longitude = json['longitude']
        self.timezone = json['timezone']
        self.timezone_short = json['timezone_abbreviation']
        self.elevation = json['elevation']
        self.units = ['hourly_units']
        self.hourly_prefixes = json['hourly_units'].keys()
        self.hours = HourOwner(json['hourly'], self.timezone)              
#        self.dissect_hours(json['hourly'])
#        self.hours = Hours(categories=self.hourly_prefixes, data=json['hourly'], timezone=self.timezone)


class HourOwner():
    def __init__(self, json_hourly, tz):
        self.categories = list(json_hourly.keys())
        self.timezone = tz
        self.hour_dict = {}
        self.hour_list = [Hour() for _ in range(len(json_hourly[self.categories[0]]))]
        for category, value_list in json_hourly.items():
            for index, value in enumerate(value_list):
                self.hour_list[index].add(category, value)
        for hour in self.hour_list:
#            hour.info['time'] = datetime.strptime(hour.info['time'],"%Y-%m-%dT%H:%M")
            self.hour_dict[hour.info['time']] = hour
        print(self.hour_dict)
class Hour():
    def __init__(self):
        self.info = {}
    def add(self, index, value):
        self.info[index] = value
    def __repr__(self):
        return "Hour Object at " + str(self.info['time'])
    def get(self, category):
        return self.info[category]