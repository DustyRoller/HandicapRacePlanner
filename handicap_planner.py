from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path


@dataclass
class HandicapEntry:
    name: str
    estimated_time: timedelta
    start_time: timedelta = timedelta()


@dataclass
class HandicapResult:
    name: str
    estimated_time: timedelta
    position: int
    split_time: timedelta
    finish_time: timedelta = timedelta()


def calculate_result_data(input_file: Path) -> list[HandicapResult]:
    handicap_results: list[HandicapResult] = []

    with input_file.open() as f:
        for line in f.readlines():
            name, time_str, position_str, split_str = map(str, line.split(" - "))
            est_minutes, est_seconds = map(int, time_str.split(":"))
            estimated_time: timedelta = timedelta(minutes=est_minutes, seconds=est_seconds)
            split_minutes, split_seconds = map(int, split_str.split(":"))
            split_time: timedelta = timedelta(minutes=split_minutes, seconds=split_seconds)
            handicap_results.append((HandicapResult(name, estimated_time, int(position_str), split_time)))

    if not handicap_results:
        raise RuntimeError(f"Failed to read any values from {input_file}")

    sorted_handicap_results = sorted(handicap_results, key=lambda x: x.position)

    # Calculate the actual finish times.
    for i, result in enumerate(sorted_handicap_results):
        if i == 0:
            result.finish_time = result.split_time
        else:
            result.finish_time = sorted_handicap_results[i - 1].finish_time + result.split_time

    return sorted_handicap_results


def calculate_start_times(input_file: Path) -> list[HandicapEntry]:
    handicap_entries: list[HandicapEntry] = []

    with input_file.open() as f:
        for line in f.readlines():
            name, time_str = map(str, line.split(" - "))
            minutes, seconds = map(int, time_str.split(":"))
            estimated_time: timedelta = timedelta(minutes=minutes, seconds=seconds)
            handicap_entries.append(HandicapEntry(name, estimated_time))

    if not handicap_entries:
        raise RuntimeError(f"Failed to read any values from {input_file}")

    sorted_handicap_entries: list[HandicapEntry] = sorted(handicap_entries, key=lambda x: x.estimated_time, reverse=True)

    race_start_time: timedelta = timedelta(hours=12)

    for i, entry in enumerate(sorted_handicap_entries):
        if i == 0:
            entry.start_time = race_start_time
        else:
            previous_entry: HandicapEntry = sorted_handicap_entries[i - 1]
            entry.start_time = previous_entry.start_time + (previous_entry.estimated_time - entry.estimated_time)

    return sorted_handicap_entries


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser, Namespace, _MutuallyExclusiveGroup

    parser: ArgumentParser = ArgumentParser(
                    prog='Handicap race planner',
                    description='Plan a handicap race')

    query_group: _MutuallyExclusiveGroup = parser.add_mutually_exclusive_group(required=True)
    query_group.add_argument("--times", type=Path, help="Path to the file with predicted times")
    query_group.add_argument("--results", type=Path, help="Path to the file with the result times")

    args: Namespace = parser.parse_args()

    if args.times:
        if not args.times.is_file():
            sys.exit(f"File does not exist: {args.times}")

        entries: list[HandicapEntry] = calculate_start_times(args.times)

        for entry in entries:
            print(f"{entry.name} - {entry.start_time}")
    else:
        if not args.results.is_file():
            sys.exit(f"File does not exist: {args.results}")

        results: list[HandicapResult] = calculate_result_data(args.results)

        for result in results:
            diff: timedelta = result.finish_time - result.estimated_time
            sign: str = "+" if diff.total_seconds() >= 0 else "-"

            print(f"{result.name} - {result.estimated_time} - {result.finish_time} - {sign}{abs(diff)}")
