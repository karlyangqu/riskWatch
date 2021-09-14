import sys
sys.path.append(".")

from timeRW.frequency import Frequency
from timeRW.timeunit import TimeUnit
from core.error import RW_Ensure, RW_Fail

from multipledispatch import dispatch


class Period:

    @dispatch()
    def __init__(self) -> None:
        self._length = 0
        self._units = TimeUnit.Days

    @dispatch((int,float), TimeUnit)
    def __init__(self, n_, units_) -> None:
        self._length = n_
        self._units = units_


    @dispatch(Frequency)
    def __init__(self, frequency_) -> None:
        
        if frequency_ is Frequency.NoFrequency:
            self._units = TimeUnit.Days
            self._length = 0

        elif frequency_ is Frequency.Once:
            self._units = TimeUnit.Years
            self._length = 0

        elif frequency_ is Frequency.Annual:
            self._units = TimeUnit.Years
            self._length = 1

        elif frequency_ in [Frequency.Semiannual, Frequency.EveryFourthMonth, 
                            Frequency.Quarterly, Frequency.Bimonthly, Frequency.Monthly]:
            f = frequency_.value
            self._units = TimeUnit.Months
            self._length = 12/f

        elif frequency_ in [Frequency.EveryFourthWeek, Frequency.Biweekly, Frequency.Weekly]:
            f = frequency_.value
            self._units = TimeUnit.Weeks
            self._length = 52/f
        
        elif frequency_ is Frequency.Daily:
            self._units = TimeUnit.Days
            self._length = 1
        
        elif frequency_ is Frequency.OtherFrequency:
            RW_Fail("unknown frequency")

        else:
            RW_Fail("unknown frequency")

    def length(self):
        return self._length

    def units(self):
        return self._units

    def frequency(self):
        length_ = abs(self._length)
        units_ = self._units

        if (length_ == 0):
            if units_ == TimeUnit.Years:
                return Frequency.NoFrequency

        if units_ is Frequency.Annual:
            if length_ == 1:
                return Frequency.Annual
            else:
                return Frequency.OtherFrequency
        elif units_ is TimeUnit.Months:
            if (12%length_ == 0 and length_ <= 12):
                return Frequency(12/length_)
            else:
                return Frequency.OtherFrequency

        elif units_ is TimeUnit.Weeks:
            if length_ == 1:
                return Frequency.Weekly
            elif length_ == 2:
                return Frequency.Biweekly
            elif length_ == 4:
                return Frequency.EveryFourthWeek
            else:
                return Frequency.OtherFrequency
        
        elif units_ is TimeUnit.Days:
            if length_ == 1:
                return Frequency.Daily
            else:
                return Frequency.OtherFrequency
        
        else: 
            RW_Fail("unknown frequency")

    def normalize(self):
        if self._length != 0:
            if self._units is TimeUnit.Months:
                if (self._length % 12) == 0:
                    self._length = self._length / 12
                    self._units = TimeUnit.Years
            elif self._units in [TimeUnit.Days, TimeUnit.Weeks, TimeUnit.Years]:
                pass
            else:
                RW_Fail("unknow time unit")
    
    @staticmethod
    def years(p):
        if isinstance(p,Period):

            if p.length() == 0:
                return 0
            if p.units() is TimeUnit.Days:
                RW_Fail("Cannot convert Days into Years")
            elif p.units() is TimeUnit.Weeks:
                RW_Fail("Cannot convert Weeks into Years")
            elif p.units() is TimeUnit.Months:
                return p.length()/12.0
            elif p.units() is TimeUnit.Years:
                return p.length()
            else:
                RW_Fail("unknow time unit")

        RW_Fail("Years: input has to be Period, {0} inputted".format(type(p)))

        

    @staticmethod
    def months(p):
        if isinstance(p,Period):

            if p.length() == 0:
                return 0
            if p.units() is TimeUnit.Days:
                RW_Fail("Cannot convert Days into Months")
            elif p.units() is TimeUnit.Weeks:
                RW_Fail("Cannot convert Weeks into Months")
            elif p.units() is TimeUnit.Months:
                return p.length()
            elif p.units() is TimeUnit.Years:
                return p.length() * 12
            else:
                RW_Fail("unknow time unit")

        RW_Fail("input has to be Period, {0} inputted".format(type(p)))

    @staticmethod
    def weeks(p):
        if isinstance(p,Period):

            if p.length() == 0:
                return 0
            if p.units() is TimeUnit.Days:
                return p.length()/7
            elif p.units() is TimeUnit.Weeks:
                return p.length()
            elif p.units() is TimeUnit.Months:
                RW_Fail("Cannot convert Months into Weeks")
            elif p.units() is TimeUnit.Years:
                RW_Fail("Cannot convert Years into Weeks")
            else:
                RW_Fail("unknow time unit")

        RW_Fail("input has to be Period, {0} inputted".format(type(p)))

    @staticmethod
    def days(p):
        if isinstance(p,Period):

            if p.length() == 0:
                return 0
            if p.units() is TimeUnit.Days:
                return p.length()
            elif p.units() is TimeUnit.Weeks:
                return p.length()*7
            elif p.units() is TimeUnit.Months:
                RW_Fail("Cannot convert Months into Days")
            elif p.units() is TimeUnit.Years:
                RW_Fail("Cannot convert Years into Days")
            else:
                RW_Fail("unknow time unit")

        RW_Fail("input has to be Period, {0} inputted".format(type(p)))

    def __str__(self):
        return "Period: {0} {1}".format(self._length, self._units)

    def __eq__(self, other):
        return not ((self < other) or (other < self))  

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self,other):
        
        if isinstance(other,Period):
            
            if self.length() == 0:
                return other.length() > 0 
            
            if other.length() == 0:
                return self.length() < 0

            if self.units() == other.units():
                return self.length() < other.length()
            
            if self.units() == TimeUnit.Months and other.units() == TimeUnit.Years:
                return self.length() < 12 * other.length()

            if self.units() == TimeUnit.Years and other.units() == TimeUnit.Months:
                return 12 * self.length() < other.length()

            if self.units() == TimeUnit.Days and other.units() == TimeUnit.Weeks:
                return self.length() < 7 * other.length()

            if self.units() == TimeUnit.Weeks and other.units() == TimeUnit.Days:
                return 7 * self.length() < other.length()

            selflim = Period.daysMinMax(self)
            otherlim = Period.daysMinMax(other)

            if (selflim[1] < otherlim[0]):
                return True
            elif (selflim[0] > otherlim[1]):
                return False
            else:
                RW_Fail("undecidable comparison between {0} and {1}".format(self, other));

        RW_Fail("impossible compare < between {0} and {1}".format(self, other))
        

    def __gt__(self,other):
        return other < self

    def __le__(self,other):
        return not(self > other)

    def __ge__(self,other):
        return not(self < other)

    def __add__(self, other):

        if isinstance(other,Period):
            
            units_ = self._units
            p = Period()

            if self._length == 0:
                p._length = other.length()
                p._units = other.units()
                
            elif other._length == 0:
                p._length = self.length()
                p._units = self.units()

            elif units_ == other.units():
                p._length = self._length + other.length()
                p._units = self.units()

            else:
                if units_ is TimeUnit.Years:
                    if other.units() is TimeUnit.Months:
                        p._units = TimeUnit.Months
                        p._length = self._length * 12 + other.units()
                    elif other.units() in [TimeUnit.Weeks, TimeUnit.Days]:
                        RW_Fail("impossible addtion between {0} and {1}".format(self._units, other._units))
                    else:
                        RW_Fail("unknown time unit")

                elif units_ is TimeUnit.Months:
                    if other.units() is TimeUnit.Years:
                        p._units = TimeUnit.Months
                        p._length = self._length + other._length * 12
                    elif other.units() is [TimeUnit.Weeks, TimeUnit.Days]:
                        RW_Fail("impossible addtion between {0} and {1}".format(self._units, other._units))
                    else:
                        RW_Fail("unknown time unit")

                elif units_ is TimeUnit.Weeks:
                    if other.units() is TimeUnit.Days:
                        p._units = TimeUnit.Days
                        p._length = self._length * 7 + other.length()
                    elif other.units() in [TimeUnit.Years, TimeUnit.Months]:
                        RW_Fail("impossible addtion between {0} and {1}".format(self._units, other._units))
                    else:
                        RW_Fail("unknown time unit")

                elif units_ is TimeUnit.Days:
                    if other.units() is TimeUnit.Weeks:
                        p._units = TimeUnit.Days
                        p._length = self._length + other._length * 7
                    elif other.units() is [TimeUnit.Years, TimeUnit.Months]:
                        RW_Fail("impossible addtion between {0} and {1}".format(self._units, other._units))
                    else:
                        RW_Fail("unknown time unit")
                else:
                    RW_Fail("unknown time unit")
            return p
                
        else:
            RW_Fail("Objects can not be added: {0} and {1}.".format(self, other))

    def __iadd__(self,other):
        result_ = self + other
        self._length = result_._length
        self._units = result_._units
        return self

    def __sub__(self, other):
        return self + (-other)

    def __isub__(self,other):
        result_ = self - other
        self._length = result_._length
        self._units = result_._units
        return self

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            len_ = int(other * self._length)
            return Period(len_, self.units())
        RW_Fail("impossible multiply between {0} and {1}".format(self, other))

    def __rmul__(self,other):
        return self.__mul__(other)

    def __neg__(self):
        return -1 * self

    def __truediv__(self,other):
        if isinstance(other, int) or isinstance(other, float):
            p = Period()
            RW_Ensure(other != 0, "cannot be divided by zero")
            if (self._length % other == 0):
                p._length = int(self._length/other)
                p._units = self._units
            else:
                units_ = self._units
                length_ = self._length
                if units_ is TimeUnit.Years:
                    length_ = self._length * 12
                    units_ = TimeUnit.Months
                elif units_ is TimeUnit.Weeks:
                    length_= self._length * 7 
                    units_ = TimeUnit.Days
                
                RW_Ensure(length_ % other == 0 , "{0} cannot be divided by {1}".format(self,other))
            
                p._length = int(length_/other)
                p._units = units_

            return p

        RW_Fail("impossible divide {0} by {1}".format(self, other))

    def __idiv__(self,other):
        result_ = self / other
        self._length = result_._length
        self._units = result_._units
        return self

    @staticmethod
    def daysMinMax(p):
        if isinstance(p,Period):
            if p.units() is TimeUnit.Days:
                return (p.length(), p.length())
            elif p.units() is TimeUnit.Weeks:
                return (7 * p.length(), 7 * p.length())
            elif p.units() is TimeUnit.Months:
                return (28 * p.length(), 31 * p.length())
            elif p.units() is TimeUnit.Years:
                return (365 * p.length(), 366 * p.length())
            else:
                RW_Fail("unknown time unit")
                
        RW_Fail("impossible to find min and max date")


if __name__ == "__main__":
    p1 = Period(1, TimeUnit.Days)
    print(type(p1) is Period)
    print(p1)
    print(-p1)

    p2 = Period(2, TimeUnit.Weeks)
    print(p2)
    print("Add ->", p1 + p2)
    print("Substract ->", p1 - p2)
    print("Multiply ->", p2 * 2)
    print("Divide ->", p2 / 2)

    print("Equal ->", p1 == p2)
    print("Less ->", p1 < p2)

    p1 += p2
    print(p1)
    p1 -= p2
    print(p1)
    p1 /= 1
    print(p1)

    print(Period.days(p1))
    print(Period.weeks(p1))