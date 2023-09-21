from datetime import datetime 
import pytz 
import json
import os 


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
    def __init__(self, filename = "mods.json"):
        if not os.path.isfile(filename):
            with open(filename, 'w') as fp:
                json.dump({},fp)
        with open(filename, 'r') as fp:
            self.info = json.load(fp)
        self.timespans = {}
    def feed_hourly_info(self, hours):
        for attr in hours[0].info.keys():
            if attr == 'time':
                continue
            self.timespans[attr] = TimespanData(attr, hours)

    def get_recommendation(self, user='1'):
        wind_mod = self.info[user]['Coefficients']['WindspeedSens']
        humid_mod = self.info[user]['Coefficients']['HumiditySens']
        temp_mod = self.info[user]['Coefficients']['TemperatureSens']

        temp = CtoF(self.timespans['temperature_2m'].average)
        wind = self.timespans['windspeed_10m'].average
        humid = self.timespans['relativehumidity_2m'].average

        att = Attire()
        # base layer
        print("RECOMMENDATION:")
        match temp + temp_mod:
            case val if val > 10:
                att.shirt = "Tshirt"
            case val if val <= 10:
                att.shirt = "Secondskin"
        # outer layer
        match temp + temp_mod:
            case val if val > 65:
                pass
            case val if 55 < val <= 65:
                att.sweater = "Light Sweatshirt"
            case val if 45 < val <= 55:
                att.sweater = "Heavy Sweatshirt"
            case val if 30 < val <= 45:
                att.sweater = "Jacket"
            case val if val <= 30:
                att.sweater = "Coat"
        # pants
        match temp + temp_mod:
            case val if val > 50:
                att.legs = "Shorts"
            case val if 10 < val <= 50:
                att.legs = "Pants"
            case val if val <= 10:
                att.legs = "Long Underwear"
        match temp + temp_mod:
            case val if val < 0: # | if snowing:
                att.outerpants = "Snowpants"
        match temp + temp_mod:
            case val if 30 < val < 45:
                print("Hood")
            case val if val <= 30:
                print("Hat")
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
