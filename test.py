from classes import FuzzyRecallDict, BinarySearch
from datetime import datetime 
import pandas
from sklearn import linear_model

def main():
    t1 = FuzzyRecallDict()
    for i in range(0, 2000, 100):
        t1[i] = str(i)

    assert t1[100] == '100'
    assert t1[1900] == '1900'
    assert t1[501] == '500'
    assert t1[550] == '500'
    assert t1[590] == '500'

    t2 = FuzzyRecallDict()
    for i in range(0, 20):
        t2[datetime(2023, 9, 19, i, 0, 0)] = str(i)
    
    assert t2[datetime(2023, 9, 19, 5, 0, 0)] == '5'
    assert t2[datetime(2023, 9, 19, 19, 0, 0)] == '19'
    assert t2[datetime(2023, 9, 19, 4, 32, 16)] == '4'
    assert t2[datetime(2023, 9, 20, 0, 0, 0)] == '19'


    value = 50
    match value:
        case val if val < 5:
            print("a")
        case val if 5 <= val < 20:
            print('b')
        case val if val >= 20:
            print('c')

    data = {"A": [5,4,5,6,3,],
            "B": [10,9,11,12,8],
            "C": [1,0,1,1,0],}
    data2 = {
        "Temperature":[],
        "Windspeed":[],
        "Humidity":[],
        "Cloudcover":[],
        "UV Index":[],
        "Activity Level":[]
    }

    df = pandas.DataFrame(data)
    print(df)
    X = df[['A','B']]
    y = df['C']


    regr = linear_model.LogisticRegression()
    regr.fit(X,y)

    pred = regr.predict([[4,100]])
    print(pred)
    print(regr.coef_)


if __name__ == "__main__":
    main()