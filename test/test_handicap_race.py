from pathlib import Path
from unittest import TestCase

from handicap_planner import calculate_result_data, calculate_start_times


class TestHandicapPlanner(TestCase):
    def test_calculate_start_times_raises_error_if_file_is_empty(self):
        test_file_path = Path("testdata.txt")

        with Path.open(test_file_path, "w"):
            pass

        with self.assertRaises(RuntimeError) as err:
            calculate_start_times(test_file_path)

        self.assertTrue(f"Failed to read any values from {test_file_path}" in str(err.exception))

        Path.unlink(test_file_path)

    def test_calculate_start_times_raises_error_if_data_is_malformed(self):
        test_file_path = Path("testdata.txt")

        with Path.open(test_file_path, "w") as f:
            f.write("a\n")
            f.write("26:00\n")
            f.write("c - 24:00\n")

        with self.assertRaises(ValueError) as _:
            calculate_start_times(test_file_path)

        Path.unlink(test_file_path)

    def test_calculate_start_times_raises_error_if_time_is_malformed(self):
        test_file_path = Path("testdata.txt")

        with Path.open(test_file_path, "w") as f:
            f.write("a - 26-00\n")
            f.write("b - 26:00\n")
            f.write("c - 24:00\n")

        with self.assertRaises(ValueError) as _:
            calculate_start_times(test_file_path)

        Path.unlink(test_file_path)

    def test_calculate_start_times_returns_expected_results(self):
        test_file_path = Path("testdata.txt")

        with Path.open(test_file_path, "w") as f:
            f.write("a - 25:00\n")
            f.write("b - 26:30\n")
            f.write("c - 24:00\n")

        handicap_entries = calculate_start_times(test_file_path)

        self.assertEqual(3, len(handicap_entries))
        self.assertEqual("b", handicap_entries[0].name)
        self.assertEqual("12:00:00", str(handicap_entries[0].start_time))
        self.assertEqual("a", handicap_entries[1].name)
        self.assertEqual("12:01:30", str(handicap_entries[1].start_time))
        self.assertEqual("c", handicap_entries[2].name)
        self.assertEqual("12:02:30", str(handicap_entries[2].start_time))

        Path.unlink(test_file_path)

    def test_calculate_result_data_raises_error_if_file_is_empty(self):
        test_file_path = Path("testdata.txt")

        with Path.open(test_file_path, "w"):
            pass

        with self.assertRaises(RuntimeError) as err:
            calculate_result_data(test_file_path)

        self.assertTrue(f"Failed to read any values from {test_file_path}" in str(err.exception))

        Path.unlink(test_file_path)

    def test_calculate_result_data_raises_error_if_data_is_malformed(self):
        test_file_path = Path("testdata.txt")

        with Path.open(test_file_path, "w") as f:
            f.write("a\n")
            f.write("26:00\n")
            f.write("c - 24:00\n")

        with self.assertRaises(ValueError) as _:
            calculate_result_data(test_file_path)

        Path.unlink(test_file_path)

    def test_calculate_result_data_raises_error_if_time_is_malformed(self):
        test_file_path = Path("testdata.txt")

        with Path.open(test_file_path, "w") as f:
            f.write("a - 26-00 - 2\n")
            f.write("b - 26:00 - 1\n")
            f.write("c - 24:00 - 3\n")

        with self.assertRaises(ValueError) as _:
            calculate_result_data(test_file_path)

        Path.unlink(test_file_path)

    def test_calculate_result_data_returns_expected_results(self):
        test_file_path = Path("testdata.txt")

        with Path.open(test_file_path, "w") as f:
            f.write("a - 12:00:00 - 25:00 - 1 - 15:00\n")
            f.write("b - 12:00:30 - 26:30 - 3 - 1:00\n")
            f.write("c - 12:01:25 - 24:00 - 2 - 0:30\n")

        handicap_entries = calculate_result_data(test_file_path)

        self.assertEqual(3, len(handicap_entries))
        self.assertEqual("a", handicap_entries[0].name)
        self.assertEqual("0:15:00", str(handicap_entries[0].split_time))
        self.assertEqual("0:15:00", str(handicap_entries[0].finish_time))
        self.assertEqual("0:15:00", str(handicap_entries[0].race_time))
        self.assertEqual("c", handicap_entries[1].name)
        self.assertEqual("0:00:30", str(handicap_entries[1].split_time))
        self.assertEqual("0:15:30", str(handicap_entries[1].finish_time))
        self.assertEqual("0:14:05", str(handicap_entries[1].race_time))
        self.assertEqual("b", handicap_entries[2].name)
        self.assertEqual("0:01:00", str(handicap_entries[2].split_time))
        self.assertEqual("0:16:30", str(handicap_entries[2].finish_time))
        self.assertEqual("0:16:00", str(handicap_entries[2].race_time))

        Path.unlink(test_file_path)
