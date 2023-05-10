class Forecast():
    def __init__(self, json):
        # Location information
        self.latitude = json['latitude']
        self.longitude = json['longitude']
        self.timezone = json['timezone']
        self.units = ['hourly_units']
        self.hourly_prefixes = json['hourly_units'].keys()
        self.hours = Hours(categories=self.hourly_prefixes, data=json['hourly'])


class Hours():
    def __init__(self, categories=[],data={}):
        self.cats = list(categories)
        self.hours = []
        for i in range(0, len(data[self.cats[0]])):
            new_hour = Hour()
            for category in self.cats:
                new_hour.add(category, data[category][i])
            self.hours.append(new_hour)


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