from datetime import datetime, timedelta

import pytest

from app.vos import ScheduledEventVO


class TestScheduledEventVO:
    TEST_NAME = "event name"
    TEST_START_DATE = datetime.fromisoformat("2012-07-03 14:00")
    TEST_END_DATE = datetime.fromisoformat("2012-07-03 14:00")
    TEST_PLACE = "event's place, CITY"
    TEST_REMARKS = "event's place"
    TEST_LOCALE = "en_uk"
    TEST_HOURS = ["01:00", "01:33", "11:59", "12:00", "17:00", "23:59"]
    TEST_YEARS = [
        datetime.fromisoformat("2012-07-03 14:00"),
        datetime.fromisoformat("2037-07-03 14:00"),
    ]

    @classmethod
    def get_test_scheduled_event(
        cls,
        name: str = TEST_NAME,
        start_date: datetime = TEST_START_DATE,
        end_date: datetime = TEST_END_DATE,
        place: str = TEST_PLACE,
        remarks: str = TEST_REMARKS,
        locale: str = TEST_LOCALE,
    ):
        return ScheduledEventVO(
            name=name,
            start_date=start_date,
            end_date=end_date,
            place=place,
            remarks=remarks,
            locale=locale,
        )

    @pytest.mark.parametrize(
        "weekday, locale, expected_name",
        [
            (0, "en_uk", "Monday"),
            (1, "en_uk", "Tuesday"),
            (2, "en_uk", "Wednesday"),
            (3, "en_uk", "Thursday"),
            (4, "en_uk", "Friday"),
            (5, "en_uk", "Saturday"),
            (6, "en_uk", "Sunday"),
            (0, "pl", "poniedziałek"),
            (1, "pl", "wtorek"),
            (2, "pl", "środa"),
            (3, "pl", "czwartek"),
            (4, "pl", "piątek"),
            (5, "pl", "sobota"),
            (6, "pl", "niedziela"),
        ],
    )
    def test_start_weekday(self, weekday: int, locale: str, expected_name: str):
        # Given
        # https://stackoverflow.com/a/1622263
        start_date = self.TEST_START_DATE + timedelta(
            days=-self.TEST_START_DATE.weekday() + weekday
        )
        assert start_date.weekday() == weekday
        scheduled_event = self.get_test_scheduled_event(
            start_date=start_date, locale=locale
        )
        # Then
        assert scheduled_event.start_date_weekday == expected_name

    @pytest.mark.parametrize(
        "start_date, expected",
        [
            (datetime.fromisoformat("2012-07-03 14:00"), 3),
            (datetime.fromisoformat("2012-06-14 14:00"), 14),
        ],
    )
    def test_start_day_of_the_month(self, start_date, expected):
        # Given
        scheduled_event = self.get_test_scheduled_event(start_date=start_date)
        # Then
        assert scheduled_event.start_date_day_of_the_month == expected

    @pytest.mark.parametrize(
        "month_number, roman_number",
        [
            (1, "I"),
            (2, "II"),
            (3, "III"),
            (4, "IV"),
            (5, "V"),
            (6, "VI"),
            (7, "VII"),
            (8, "VIII"),
            (9, "IX"),
            (10, "X"),
            (11, "XI"),
            (12, "XII"),
        ],
    )
    def test_start_date_month_roman(self, month_number, roman_number):
        # Given
        start_date = datetime.fromisoformat(f"2000-{month_number:>02}-03 14:00")
        scheduled_event = self.get_test_scheduled_event(start_date=start_date)
        # Then
        assert scheduled_event.start_date_month_roman == roman_number

    @pytest.mark.parametrize("start_date", TEST_YEARS)
    def test_start_date_year(self, start_date):
        event = self.get_test_scheduled_event(start_date=start_date)
        # Then
        assert event.start_date_year == start_date.year

    @pytest.mark.parametrize("hour", TEST_HOURS)
    def test_start_date_hour(self, hour):
        # Given
        start_date = datetime.fromisoformat(f"2012-07-03 {hour}")
        event = self.get_test_scheduled_event(start_date=start_date)
        # Then
        assert event.start_date_hour == hour

    @pytest.mark.parametrize("hour", TEST_HOURS)
    def test_end_date_hour(self, hour):
        # Given
        end_date = datetime.fromisoformat(f"2012-07-03 {hour}")
        event = self.get_test_scheduled_event(end_date=end_date)
        # Then
        assert event.end_date_hour == hour

    def test_place_without_city(self):
        # Given
        street = "3rd Happy st"
        city = "Lemoyne"
        place = f"{street} {city}"
        event = self.get_test_scheduled_event(place=place)
        # Then
        assert event.place_without_city == street

    def test_place_city(self):
        # Given
        street = "3rd Happy st"
        city = "Lemoyne"
        place = f"{street} {city}"
        event = self.get_test_scheduled_event(place=place)
        # Then
        assert event.place_city == city
