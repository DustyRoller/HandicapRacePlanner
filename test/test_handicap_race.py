from pathlib import Path
from unittest import TestCase

from handicap_planner import calculate_start_times


class TestHandicapPlanner(TestCase):
    def test_calculate_start_times_errors_if_file_is_empty(self):
        test_file_path = "testdata.txt"

        with Path.open(test_file_path, "w"):
            pass

        with self.assertRaises(RuntimeError) as err:
            calculate_start_times(test_file_path)

        self.assertTrue(f"Failed to read any values from {test_file_path}" in str(err.exception))

        Path.unlink(test_file_path)

    def test_calculate_start_times_errors_if_data_is_malformed(self):
        test_file_path = "testdata.txt"

        with Path.open(test_file_path, "w") as f:
            f.write("a\n")
            f.write("26:00\n")
            f.write("c - 24:00\n")

        with self.assertRaises(ValueError) as _:
            calculate_start_times(test_file_path)

        Path.unlink(test_file_path)

    def test_calculate_start_times_errors_if_time_is_malformed(self):
        test_file_path = "testdata.txt"

        with Path.open(test_file_path, "w") as f:
            f.write("a - 26-00\n")
            f.write("b - 26:00\n")
            f.write("c - 24:00\n")

        with self.assertRaises(ValueError) as _:
            calculate_start_times(test_file_path)

        Path.unlink(test_file_path)

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
