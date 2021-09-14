import sys 
sys.path.append(".")

from patterns.observable import Observable
from core.event import Event
from timeRW.date import Date
from core.settings import Settings
from core.error import RW_Ensure, RW_TypeCheck


class Event(Observable):

    def __init__(self):
        self._date = None 

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, date_):
        self._date = date_

    def hasOccurred(self, date_, includeRefDate_ = None):

        if date_ != Date():
            refDate = date_
        else:
            refDate = Settings().instance().evaluationDate()

        if includeRefDate_ is None:
            includeRefDate_ = Settings().instance().includeReferenceDateEvents()

        if includeRefDate_:
            return Date() < refDate
        else:
            return Date() <= refDate 

    def accept(self, visitor_):
        RW_TypeCheck(type(visitor_), Event,"not an event visitor")
        visitor_.visit(self)


class simple_event(Event):

    def __init__(self,date_):
        self._date = date_