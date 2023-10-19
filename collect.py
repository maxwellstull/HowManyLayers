from main import getOpenMeteo 
from classes import BaseLayer, OuterLayer, Legs, Activity, associations, Forecast
import pandas as pd
import datetime


def addData():
    data = pd.read_csv('train.csv')

    association_i = dict([(value, key) for key, value in associations.items()])

    weather = Forecast(getOpenMeteo())
    current_time = datetime.datetime.now()
    weather_now = weather.getHour(current_time)
    
    new_row = {}

    for col in data.columns:
        if col in association_i.keys():
            new_row[col] = [weather_now.get(association_i[col])]
        else:
            match col:
                case "Activity":
                    print("Select activity level")
                    for level in Activity:
                        print("{:12}: {:2}".format(level.name, level.value))
                    inp = int(input("> "))
                    new_row[col] = inp
                case "Base":
                    print("Select base layer")
                    for level in BaseLayer:
                        print("{:12}: {:2}".format(level.name, level.value))
                    inp = int(input("> "))
                    new_row[col] = inp
                case "Outer":
                    print("Select outer layer")
                    for level in OuterLayer:
                        print("{:12}: {:2}".format(level.name, level.value))
                    inp = int(input("> "))
                    new_row[col] = inp
                case "Legs":
                    print("Select legs layer")
                    for level in Legs:
                        print("{:12}: {:2}".format(level.name, level.value))
                    inp = int(input("> "))
                    new_row[col] = inp
    


    df = pd.DataFrame(new_row)
    data = pd.concat([data, df], ignore_index=True)
    print(data)
    
    data.to_csv('train.csv')

if __name__ == "__main__":
    addData()