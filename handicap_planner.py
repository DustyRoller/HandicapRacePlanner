from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path


@dataclass
class HandicapEntry:
    name: str
    estimated_time: timedelta
    start_time: timedelta = timedelta()


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
    from argparse import ArgumentParser, Namespace

    parser: ArgumentParser = ArgumentParser(
                    prog='Handicap race planner',
                    description='Plan a handicap race')

    parser.add_argument("--times", required=True, type=Path, help="Path to the file with predicted times")

    args: Namespace = parser.parse_args()

    if not args.times.is_file():
        exit(f"File does not exist: {args.times}")

    entries: list[HandicapEntry] = calculate_start_times(args.times)

    for entry in entries:
        print(f"{entry.name} - {entry.start_time}")
