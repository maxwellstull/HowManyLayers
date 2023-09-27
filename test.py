from classes import FuzzyRecallDict, BinarySearch
from datetime import datetime 


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





if __name__ == "__main__":
    main()