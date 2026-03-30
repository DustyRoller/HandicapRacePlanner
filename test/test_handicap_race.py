from pathlib import Path
from unittest import TestCase

from handicap_planner import calculate_start_times


class TestHandicapPlanner(TestCase):
    def test_calculate_start_times_returns_expected_results(self):
        test_file_path = "testdata.txt"

        with Path.open(test_file_path, "w") as f:
            f.write("a - 25:00\n")
            f.write("b - 26:00\n")
            f.write("c - 24:00\n")

        start_times = calculate_start_times(test_file_path)

        self.assertEqual(3, len(start_times))
        self.assertEqual("b", start_times[0][0])
        self.assertEqual("12:00:00", str(start_times[0][1]))
        self.assertEqual("a", start_times[1][0])
        self.assertEqual("12:01:00", str(start_times[1][1]))
        self.assertEqual("c", start_times[2][0])
        self.assertEqual("12:02:00", str(start_times[2][1]))

        Path.unlink(test_file_path)
