
import sys 
sys.path.append(".")

from patterns.singleton import Singleton
from timeRW.date import Date

class Settings(object, metaclass=Singleton):

    def __init__(self):
        self._evaluationDate = Date()
        self._includeReferenceDateEvents = False

    def instance(self):
        return self

    def evaluationDate(self):
        return self._evaluationDate

    def includeReferenceDateEvents(self):
        return self._includeReferenceDateEvents



if __name__ == "__main__":

    date_ = Settings().evaluationDate()
    print(date_)
    print("succeed")