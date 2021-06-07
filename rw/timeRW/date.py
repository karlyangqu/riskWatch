
from datetime import date, datetime

class Date:
    def __init__(self, date = None) -> None:
        if date is None:
            # implement configuration date as well
            self._date = datetime.today()
        else:
            self._date = date

    def __call__(self, *args, **kwds):
        if self._date is None:
            return datetime.today()
        return self._date


if __name__ == "__main__":
    date = Date()
    print(date())