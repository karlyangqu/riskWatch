import sys 
sys.path.append(".")

from enum import Enum, auto
from timeRW.date import Date

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
        return self.date(index_)

    def dates(self):
        return self._dates

    def lastDate(self):
        return self._dates[-1]

class EarlyExercise(Exercise):
    pass

class AmericanExercise(EarlyExercise):
    pass

class BermudanExercise(EarlyExercise):
    pass

class EuropeanExecrise(Exercise):
    pass

if __name__ == "__main__":
    print(ExerciseType.American)