import datetime
import typing




class TradeDayMapping:
    day: int
    real_date: datetime.date

    def __init__(self, day: int, real_date: typing.Union[str, datetime.date]):
        if isinstance(real_date, str):
            real_date = datetime.datetime.strptime(real_date, "%Y-%m-%d").date()

        if isinstance(real_date, datetime.datetime):
            real_date = real_date.date()

        if not isinstance(real_date, datetime.date):
            raise ValueError(f"real date not datetime.date")

        self.day = day
        self.real_date = real_date

    def __eq__(self, other):
        if isinstance(other, TradeDayMapping):
            return self.day == other.day and self.real_date == other.real_date
        return False

    def __str__(self):
        return f"{self.day}: {self.real_date}"

    def __repr__(self):
        return str(self)


