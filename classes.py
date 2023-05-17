from datetime import datetime 

class Forecast():
    def __init__(self, json):
        # Location information
        self.latitude = json['latitude']
        self.longitude = json['longitude']
        self.timezone = json['timezone']
        self.units = ['hourly_units']
        self.hourly_prefixes = json['hourly_units'].keys()
        self.hours = Hours(categories=self.hourly_prefixes, data=json['hourly'], timezone=self.timezone)


class Hours():
    def __init__(self, categories=[],data={}, timezone=""):
        self.cats = list(categories)
        self.timezone = timezone
        self.hours = {}
        self.hours_list = []
        for i in range(0, len(data[self.cats[0]])):
            new_hour = Hour()
            for category in self.cats:
                new_hour.add(category, data[category][i])
            self.hours_list.append(new_hour)
            self.hours[data['time'][i]] = new_hour
            time_obj = datetime.strptime(data['time'][i],"%Y-%m-%dT%H:%M")
            time_obj = time_obj.replace(tzinfo = self.timezone)
            print(time_obj)
            print(time_obj.tzinfo)
    # Returns list of the given category
    def get_plottable(self, category):
        retval = []
        for i in range(0, len(self.hours_list)):
            retval.append(self.hours_list[i].get(category))
        return retval


class Hour():
    def __init__(self):
        self.info = {}
    def add(self, index, value):
        self.info[index] = value
    def __repr__(self):
        retval = str(self.info['time']) + '\n'
        for key, value in self.info.items():
            retval += "\t{k}: {v}\n".format(k=key,v=value)
        return retval
    def get(self, category):
        return self.info[category]