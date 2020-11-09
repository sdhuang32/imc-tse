#!/usr/bin/env python3

from spacex import SpaceXData
import unittest

class SpaceXDataTest(unittest.TestCase):
    def test_heaviest_flight_in_date_range(self):
        """
        Example test cases for the two methods added in class SpaceXData:
            get_launch_date_range
            &
            get_heaviest_launch
        """
        spx = SpaceXData()

        try:
            spx.get_launch_date_range("2019-aa-bb", "2019-01-05")
            spx.get_launch_date_range("2019-01-01", "20201230")
        except ValueError:
            # Correct, invalid date format, we should error.
            pass
        else:
            assert False, "Invalid date format, should raise ValueError!"

        assert spx.get_launch_date_range("2019-01-01", "2019-01-05") == None
        assert spx.get_heaviest_launch("2019-01-01", "2019-01-05") == None

        flights = spx.get_launch_date_range("2019-01-01", "2020-06-01")
        self.assertIsInstance(flights, list)

        flight = spx.get_heaviest_launch("2019-01-01", "2020-06-01")
        self.assertIsInstance(flight, dict)
        assert flight.get('flight_number') == 84

if __name__ == "__main__":
    unittest.main()
