from datetime import datetime 
import pytz 
import json
import os 

class Recommender():
    def __init__(self, filename = "mods.json"):
        if not os.path.isfile(filename):
            with open(filename, 'w') as fp:
                json.dump({},fp)
        with open(filename, 'r') as fp:
            self.info = json.load(fp)
        
    def get_recommendation(self, weatherHour, user=1):
        wind = self.info[user]['Coefficients']['WindspeedSens']
        humid = self.info[user]['Coefficients']['HumiditySens']
        temp = self.info[user]['Coefficients']['TemperatureSens']
    



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
    def getHour(self, hour):
        return self.hours.getHour(hour)
    def getRelevantHours(self, req_hours, duration):
        self.hours.getRelevantHours(req_hours, duration)

class HourOwner():
    def __init__(self, json_hourly, tz):
        self.categories = list(json_hourly.keys())
        self.timezone = tz
        self.hour_dict = FuzzyRecallDict()
        self.hour_list = [Hour() for _ in range(len(json_hourly[self.categories[0]]))]
        for category, value_list in json_hourly.items():
            for index, value in enumerate(value_list):
                self.hour_list[index].add(category, value)
        for hour in self.hour_list:
            hour.info['time'] = datetime.strptime(hour.info['time'],"%Y-%m-%dT%H:%M")
            self.hour_dict[hour.info['time']] = hour
    def getHour(self, hour):
        return self.hour_dict[hour]
    def getRelevantHours(self, req_hour, duration):
        retval = []
        tmp_hour = req_hour
        for i in range(1, duration+1):
            val = self.getHour(tmp_hour)
            retval.append(val)
            tmp_hour = tmp_hour.replace(hour=req_hour.hour + i)
        print(retval)

class Hour():
    def __init__(self):
        self.info = {}
    def add(self, index, value):
        self.info[index] = value
    def __repr__(self):
        retval = "Hour Object: "
        for key, value in self.info.items():
            retval += "\t{a}: {b}\n".format(a=key, b=value)
        return retval
    def get(self, category):
        return self.info[category]
    

def BinarySearch(data, target):
    def bs(data, target):
        lb = 0
        rb = len(data)
        mid = 0
        while lb < rb:
            mid = (lb + rb) // 2
            if data[mid] < target:
                lb = mid + 1
            else:
                rb = mid

        return lb
    i = bs(data, target)
    if i:
        return i - 1
    else:
        return -1

# Dictionary wrapper that allows for some give-or-take when choosing key.
# In effect, the issue is time from the API is on the hour, and the time is
# the key. But, the time of the call is not going to be on the hour. 
# So, this dict allows for normal dict setting, but any getting will give
# the nearest hour rounded down. So FuzzyRecallDict[11:45:00] will round down to
# 11:00:00. To prevent additional setting, it gets locked.
class FuzzyRecallDict():
    def __init__(self):
        self.locked = False
        self.dict = {}
        self.key_list = []
    def __getitem__(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            result = BinarySearch(self.key_list, key)
            return self.dict[self.key_list[result]]
    def __setitem__(self, key, value):
        if self.locked == False:
            self.dict[key] = value
            self.key_list.append(key)
        else:
            print("Insertion Denied")
    def lock(self):
        self.locked = True
    def items():
        pass
