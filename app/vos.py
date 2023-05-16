from dataclasses import dataclass, field
from datetime import datetime

import roman
from babel.dates import format_date, format_datetime


@dataclass(frozen=True, slots=True)
class ScheduledEventVO:
    name: str
    start_date: datetime
    end_date: datetime
    place: str
    remarks: str
    locale: str
    _day_of_the_week_format: str = field(default="EEEE", init=False)
    _hour_format: str = field(default="HH:mm", init=False)

    # TODO ~maybe~ add post init check if start_date < end_date

    @property
    def start_date_weekday(self) -> str:
        return format_date(
            self.start_date, self._day_of_the_week_format, locale=self.locale
        )

    @property
    def start_date_day_of_the_month(self) -> int:
        return self.start_date.day

    @property
    def start_date_month_roman(self) -> str:
        return roman.toRoman(self.start_date.month)

    @property
    def start_date_year(self) -> int:
        return self.start_date.year

    @property
    def start_date_hour(self) -> str:
        return format_datetime(self.start_date, format=self._hour_format)

    @property
    def end_date_hour(self) -> str:
        return format_datetime(self.end_date, format=self._hour_format)

    @property
    def place_without_city(self) -> str:
        """We naively assume that the last word of location is a city."""
        return " ".join(self.place.split(" ")[:-1])

    @property
    def place_city(self) -> str:
        """We naively assume that the last word of location is a city."""
        return self.place.split(" ")[-1]
