from datetime import datetime 
import pytz 
import json
import os 
import pandas as pd
from sklearn import linear_model
from enum import Enum

class BaseLayer(Enum):
    SHIRT = 1           # tshirt, long sleeve
    SECONDSKIN = 2      # underarmor
class OuterLayer(Enum):
    NONE = 0
    SWEATSHIRT = 1      
    WINDBREAKER = 2
    JACKET = 3
    COAT = 4
    SUPERCOLD = 5   # sweatshirt and a coat
class Legs(Enum):
    SHORTS = 1
    PANTS = 2
    SUPERCOLD = 3   # pants and long underwear
class Activity(Enum):
    WALKING = 1
    MOVING = 2
    RUNNING = 3

associations = {"temperature_2m": "Temperature",
                "windspeed_10m": "Windspeed",
                "relativehumidity_2m":"Humidity",
                "cloudcover":"Cloudcover",
                "uv_index":"UV"}

def CtoF(cel):
    return (cel*9/5) + 32

class Attire():
    def __init__(self):
        self.shirt = ""
        self.sweater = ""
        self.complication = ""

        self.legs = ""
        self.outerpants = ""

        self.head = ""
    def __repr__(self):
        retval = """
Head: {hd:}
Torso: {sh:} {sw:} {co:}
Legs: {lg:} {ot:}
""".format(hd=self.head,sh=self.shirt,sw=self.sweater,co=self.complication,lg=self.legs,ot=self.outerpants)
        return retval

class TimespanData():
    def __init__(self, attribute, hours):
        self.collection = []
        self.attribute = attribute
        for hour in hours:
            self.collection.append(hour.info[attribute])
        self.minimum = float(min(self.collection))
        self.average = float(sum(self.collection)/len(self.collection))
        self.maximum = float(max(self.collection))
    def __repr__(self):
        retval = "{attr:<10s}: [{min:4.1f}]-[{avg:4.1f}]-[{max:4.1f}]\n".format(attr=self.attribute[:10], min=self.minimum,avg=self.average,max=self.maximum)
        return retval

class Recommender():
    def __init__(self):
#        if not os.path.isfile(filename):
#            with open(filename, 'w') as fp:
#                json.dump({},fp)
#        with open(filename, 'r') as fp:
#            self.info = json.load(fp)
        self.timespans = {}
    def train(self, filename='train.csv'):
        data = pd.read_csv(filename)        

        headers = list(associations.values()) + ['Activity']

        x_train = data[headers]

        y_train_base = data['Base']
        self.regr_b = linear_model.LogisticRegression(max_iter=10000)
        self.regr_b.fit(x_train, y_train_base)

        y_train_outer = data['Outer']
        self.regr_o = linear_model.LogisticRegression(max_iter=10000)
        self.regr_o.fit(x_train, y_train_outer)

        y_train_legs = data['Legs']
        self.regr_l = linear_model.LogisticRegression(max_iter=10000)
        self.regr_l.fit(x_train, y_train_legs)

    def LRPredict(self, data):
        base = self.regr_b.predict(data)
        outer = self.regr_o.predict(data)
        legs = self.regr_l.predict(data)
        print(BaseLayer(base).name,OuterLayer(outer).name,Legs(legs).name)

    def feed_hourly_info(self, hours):
        for attr in hours[0].info.keys():
            if attr == 'time':
                continue
            self.timespans[attr] = TimespanData(attr, hours)

    def get_recommendation(self, user='1'):
        pass

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
        return self.hours.getRelevantHours(req_hours, duration)
    def getLRList(self, req_hours):
        return self.hours.getLRList(req_hours)
class HourOwner():
    def __init__(self, json_hourly, tz):
        self.categories = list(json_hourly.keys())
        self.timezone = tz
        self.hour_dict = FuzzyRecallDict()
        self.hour_list = [Hour() for _ in range(len(json_hourly[self.categories[0]]))]
        for category, value_list in json_hourly.items():
            for index, value in enumerate(value_list):
                if category == 'temperature_2m':
                    self.hour_list[index].add(category, CtoF(value))
                else:
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
        return retval
    def getLRList(self, req_hour):
        val = self.getHour(req_hour)
        retval = {}
        for key, value in associations.items():
            retval[value] = [val.info[key]]

        return retval
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
