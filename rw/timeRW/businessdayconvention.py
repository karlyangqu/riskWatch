from enum import Enum, auto

class BusinessDayConvention(Enum):

    Following = auto()
    ModifiedFollowing = auto()
    Preceding = auto()
    ModifiedProceding = auto()
    Unadjusted = auto()
    HalfMonthModifiedFollowing = auto()
    Nearest = auto()

    def __str__(self):
        return self.name