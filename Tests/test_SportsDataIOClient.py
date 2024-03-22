import unittest
from datetime import datetime, timedelta
from Clients.SportsDataIOClient import get_last_n_days_dates


class TestGetNLastDays(unittest.TestCase):
    def test_get_last_n_days_default_offset(self):
        expected_dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%b-%d').upper() for x in range(5)]
        actual_dates = get_last_n_days_dates(5)
        self.assertEqual(actual_dates, expected_dates)

    def test_get_last_n_days_custom_offset(self):
        custom_offset = datetime(2022, 10, 1)
        expected_dates = [(custom_offset - timedelta(days=x)).strftime('%Y-%b-%d').upper() for x in range(5)]
        actual_dates = get_last_n_days_dates(5, offset=custom_offset)
        self.assertEqual(actual_dates, expected_dates)

    def test_get_last_n_days_with_zero_days(self):
        expected_dates = []
        actual_dates = get_last_n_days_dates(0)
        self.assertEqual(actual_dates, expected_dates)


if __name__ == '__main__':
    unittest.main()
