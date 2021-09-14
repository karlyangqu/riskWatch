from enum import Enum, auto

class TimeUnit(Enum):
    Days = auto()
    Weeks = auto()
    Months = auto()
    Years = auto()
    Hours = auto()
    Minutes = auto()
    Seconds = auto()
    Milliseconds = auto()
    Microseconds = auto()

    def __str__(self):
        return self.name
