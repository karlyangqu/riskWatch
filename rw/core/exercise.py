import sys 
sys.path.append(".")

from enum import Enum, auto
from timeRW.date import Date
from core.error import RW_Ensure

class ExerciseType(Enum):
    American = auto()
    Bermudan = auto()
    European = auto()

class Exercise:
    def __init__(self, type_) -> None:
        self._type = type_
        self._dates = []

    def type(self):
        return self.type
    
    def date(self, index_):
        return self._dates[index_]
    
    def dateAt(self,index_):
        return self._dates[index_]

    def dates(self):
        return self._dates

    def lastDate(self):
        return self._dates[-1]


class EarlyExercise(Exercise):
    def __init__(self, type_, payoffAtExpiry = False):
        Exercise.__init__(self, type_)
        self._payoffAtExpiry = payoffAtExpiry
    
    def payoffAtExpiry(self):
        return self._payoffAtExpiry


class AmericanExercise(EarlyExercise):
    def __init__(self, latestDate, earliestDate = None, payoffAtExpiry = False):
        EarlyExercise.__init__(self, ExerciseType.American, payoffAtExpiry)

        RW_Ensure(latestDate >= earliestDate)

        if earliestDate is None:
            self._dates.append(Date.minDate())
        else:
            self._dates.append(earliestDate)

        self._dates.append(latestDate)
        

class BermudanExercise(EarlyExercise):
    def __init__(self, dates_, payoffAtExpiry):
        RW_Ensure(len(dates_)>0, "no exercise date given")
        EarlyExercise.__init__(self, ExerciseType.Bermudan, payoffAtExpiry)
        dates_.sort()
        self._dates = dates_
        

class EuropeanExercise(Exercise):
    def __init__(self, date_):
        Exercise.__init__(self, ExerciseType.European)
        self._dates.append(date_)

if __name__ == "__main__":
    e = EuropeanExercise(Date(1,1,2000))
    print(e._dates[0]())