import sys
sys.path.append(".")

from timeRW.businessdayconvention import BusinessDayConvention

class Calendar:

    class Impl:
        
        def name(self):
            pass

        def isBusinessDay(self):
            pass

        def isWeekend(self):
            pass

        def addHoliday(self):
            pass

        def removeHoliday(self):
            pass


    def __init__(self) -> None:
        pass

    def empty(self):
        pass

    def name(self):
        pass

    def __str__(self):
        pass

    def __eq__(self, o: object) -> bool:
        pass

    def __ne__(self, o: object) -> bool:
        pass

    def addHoliday(self):
        pass

    def removeHoliday(self):
        pass

    @staticmethod
    def isBusinessDay(d):
        pass

    @staticmethod
    def isHoliday(d):
        pass

    @staticmethod
    def isWeekend(w):
        pass

    @staticmethod
    def isEndOfMonth(d):
        pass

    @staticmethod
    def endofMonth(d):
        pass

    def addHoliday(d):
        pass

    def removeHoliday(d):
        pass

    def holidayList(self, from_, to_, includeWeekEngs):
        pass

    @staticmethod
    def adjust(d, businessDayConvention = BusinessDayConvention.Following):
        print(businessDayConvention) 

    @staticmethod
    def _advance_unit(d, n, unit_, businessDayConvention = BusinessDayConvention.Following, endOfMonth = False):
        pass

    @staticmethod
    def _advance_period(d, p, businessDayConvention = BusinessDayConvention.Following, endOfMonth = False):
        pass

    @staticmethod
    def advance(*args, **kargs):
        pass

    @staticmethod
    def businessDaysBetween(from_, to_, includeFirst = True, includeLast = False):
        pass

class WesternImpl(Calendar.Impl):

    @staticmethod
    def isWeekend(weekday_):
        pass

    def easterMonday(year_):
        pass

class OrthodoxImpl(Calendar.Impl):
    
    @staticmethod
    def isWeekend(weekday_):
        pass

    def easterMonday(year_):
        pass

if __name__ == "__main__":
    print(Calendar().adjust(1))