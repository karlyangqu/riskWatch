from enum import Enum

class Weekday(Enum):

    Sunday    = 1
    Monday    = 2
    Tuesday   = 3
    Wednesday = 4
    Thursday  = 5
    Friday    = 6
    Saturday  = 7

    def __str__(self):
        return self.name