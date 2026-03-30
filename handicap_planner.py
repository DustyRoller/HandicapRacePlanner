from datetime import timedelta
from pathlib import Path


def calculate_start_times(input_file: Path) -> list[tuple[str, timedelta]]:
    estimated_times: list[str] = []
    with Path.open(input_file, "r") as f:
        for line in f.readlines():
            estimated_times.append(line)

    times: list[tuple[str, timedelta]] = []

    for estimated_time in estimated_times:
        name, time_str = map(str, estimated_time.split(" - "))
        minutes, seconds = map(int, time_str.split(":"))
        times.append((name, timedelta(minutes=minutes, seconds=seconds)))

    sorted_times: list[tuple[str, timedelta]] = sorted(times, key=lambda x: x[1], reverse=True)

    race_start_time: timedelta = timedelta(hours=12)

    start_times: list[tuple[str, timedelta]] = []

    start_times.append((sorted_times[0][0], race_start_time))

    for time in sorted_times[1:]:
        start_times.append((time[0], race_start_time + (sorted_times[0][1] - time[1])))

    return start_times


if __name__ == "__main__":
    from argparse import ArgumentParser, Namespace

    parser: ArgumentParser = ArgumentParser(
                    prog='Handicap race planner',
                    description='Plan a handicap race')

    parser.add_argument("--times", required=True, type=Path, help="Path to the file with predicted times")

    args: Namespace = parser.parse_args()

    if not args.times.is_file():
        exit(f"File does not exist: {args.times}")

    start_times: list[tuple[str, timedelta]] = calculate_start_times(args.times)

    for start_time in start_times:
        print(f"{start_time[0]} - {start_time[1]}")
