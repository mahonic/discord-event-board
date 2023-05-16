# TODO unit tests for use cases (like GenerateEventsHTML)
#  the guild object can be mocked
from datetime import date, datetime

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

    @classmethod
    def get_test_scheduled_event(cls, name: str = TEST_NAME, start_date: datetime = TEST_START_DATE, end_date: datetime = TEST_END_DATE,
                                 place: str = TEST_PLACE, remarks: str = TEST_REMARKS, locale: str = TEST_LOCALE):
        return ScheduledEventVO(
            name=name, start_date=start_date, end_date=end_date, place=place, remarks=remarks, locale=locale
        )

    def test_start_day_of_the_week(self):
        # TODO test with locale parametrised
        raise NotImplementedError()

    def test_start_day_of_the_month(self):
        raise NotImplementedError()

    def test_start_date_month_roman(self):
        raise NotImplementedError()

    def test_start_date_year(self):
        raise NotImplementedError()

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
        raise NotImplementedError()

    def test_place_city(self):
        raise NotImplementedError()
