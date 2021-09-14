import sys
sys.path.append(".")

import datetime 
from enum import Enum
from multipledispatch import dispatch
import calendar as cal
from dateutil.relativedelta import relativedelta

from core.error import RW_Ensure, RW_Fail
from timeRW.weekday import Weekday
from timeRW.timeunit import TimeUnit
from timeRW.period import Period


class Month(Enum):
    January   = 1
    February  = 2
    March     = 3
    April     = 4
    May       = 5
    June      = 6
    July      = 7
    August    = 8
    September = 9
    October   = 10
    November  = 11
    December  = 12

    def __str__(self):
        return self.name

class Date:

    def __init__(self, *args) -> None:
        if len(args) == 0:
            self._date = datetime.date.today()
            self._serialNumber = Date.datetoSerial(self._date)
        elif len(args) == 1:
            args = args[0]
            if type(args) is int or type(args) is float:
                # serial number 
                self._date = Date.serialtoDate(int(args))
                self._serialNumber = int(args)
            elif (type(args) is datetime.date) or (type(args) is datetime.datetime):
                self._date = datetime.date(args.year, args.month, args.day)
                self._serialNumber = Date.datetoSerial(self._date)
        elif len(args) == 3:
            try:
                self._date = datetime.date(args[2],args[1],args[0])
                self._serialNumber = Date.datetoSerial(self._date)
            except:
                RW_Fail("Cannot convert {0} to Date".format(args))
        else:    
            RW_Fail("Cannot convert {0} to Date, length of args is {1}.".format(args, len(args)))
    
    def __call__(self, *args, **kwds):
        if self._date is None:
            return Date(datetime.today())
        return self

    def __str__(self):
        return "Date( day:{0}, month:{1}, year:{2})".format(self.dayofMonth(),self.month(),self.year())

    def __hash__(self):
        return hash(self._date)

    def date(self):
        return self._date

    def weekday(self):
        n = [2, 3, 4, 5, 6, 7, 1][self._date.weekday()]
        weekday_ = Weekday(n)
        return weekday_

    def dayofYear(self):
        return self._date.timetuple().tm_yday

    def dayofMonth(self):
        return self._date.day

    def month(self):
        return self._date.month
    
    def year(self):
        return self._date.year

    def serialNumber(self):
        return self._serialNumber

    @staticmethod
    def serialtoDate(serialNumber):
        return datetime.date(1900,1,1) + datetime.timedelta(days = serialNumber)

    @staticmethod
    def datetoSerial(date_):
        dt = date_ - datetime.date(1900,1,1)
        return dt.days

    @staticmethod
    def timeUnit_to_deltaTime(timeUnit_):
        if timeUnit_ is TimeUnit.Years:
            return relativedelta(years=1)

        if timeUnit_ is TimeUnit.Months:
            return relativedelta(months=1)

        if timeUnit_ is TimeUnit.Weeks:
            return relativedelta(weeks=1)

        if timeUnit_ is TimeUnit.Days:
            return relativedelta(days=1)

        RW_Fail("timeUnit_to_deltaTime conversion failed: unexpected object {0}".format(type(timeUnit_)))

    @staticmethod
    def advance(d, unit_,TimeUnit_):
        relativedate_ = Date.timeUnit_to_deltaTime(TimeUnit_) * unit_ 
        return Date(d + relativedate_)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def __lt__(self,other):
        return self._date < self._date

    def __gt__(self,other):
        return self._date > self._date

    def __le__(self,other):
        return self._date <= self._date

    def __ge__(self,other):
        return self._date >= self._date

    def __add__(self,other):
        if type(other) is int or type(other) is float:
            return Date(self._serialNumber + int(other))
        elif type(other) is Period:
            return Date.advance(self,other.length(),other.units())
        RW_Fail("Unimplemented add method between {0} and {1}.".format(type(self), type(other)))

    def __radd__(self,other):
        return self.__add__(other)

    def __iadd__(self,other):
        result_ = self + other
        self._date = result_._date
        self._serialNumber = result_._serialNumber
        return self

    # ++ method can not be implemented in python 

    def __sub__(self,other):
        if type(other) is int or type(other) is float:
            return Date(self._serialNumber - int(other))
        elif type(other) is Period:
            return Date.advance(self,-other.length(),other.units())
        RW_Fail("Unimplemented substract method between {0} and {1}.".format(type(self), type(other)))

    def __isub__(self,other):
        result_ = self - other
        self._date = result_._date
        self._serialNumber = result_.serialNumber
        return self

    # -- method can not be implemented in python

    @staticmethod
    def daysBetween(d1, d2):
        return (d1 - d2).days

    @staticmethod
    def todaysDate():
        return Date()

    @staticmethod
    def minDate():
        return Date(Date._minimumSerialNumber)

    @staticmethod
    def maxDate():
        return Date(Date._maximumSerialNumber)

    @staticmethod
    def isLeap(y):
        return cal.isleap(y)
    
    @staticmethod
    def endofMonth(d):
        if (type(d) is datetime.date) or (type(d) is datetime.datetime):
           d = Date(d)

        year_ = d.year()
        month_ = d.month()
        day_ = cal.monthrange(year_, month_)[1] 

        return Date(day_,month_,year_)

    @staticmethod
    def isEndofMonth(d):
        dateEndofMonth_ = Date.endofMonth(d)
        return d == dateEndofMonth_

    @staticmethod
    def nextWeekday(d,w):
        wd = d.weekday()
        if wd.value > w.value:
            n = 7
        else:
            n = 0
        return d + (n - wd.value + w.value)

    @staticmethod
    def nthWeekday(nth,w,m,y):
        first_ = Date(1,m,y).weekday().value
        if w.value >= first_:
            n = 1
        else:
            n = 0 
        skip_ = nth - n
        return Date(1 + w.value + 7 * skip_, m, y)

    @staticmethod
    def _minimumSerialNumber():
        return 367  #Jan 1st, 1901

    @staticmethod
    def _maximumSerialNumber(): #gi
        return 109574   # Dec 31st, 2199

    @staticmethod
    def _checkSerialNumber(serialNumber_):
        RW_Ensure((serialNumber_<= Date._maximumSerialNumber) and (serialNumber_ >= Date._minimumSerialNumber),
        "Date's serial number {0} outside allowed range [{1},{2}], i.e. [{3},{4}]".format(
            serialNumber_, Date._minimumSerialNumber, Date._maximumSerialNumber, Date.minDate, Date.maxDate))

if __name__ == "__main__":
    date = Date(4, 10, 2020)
    print(date.serialNumber())
    date1 = Date(date.serialNumber())
    print(date1)
    print(Date.nextWeekday(date1,Weekday.Sunday))

