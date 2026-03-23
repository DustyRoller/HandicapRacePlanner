from pathlib import Path
from datetime import timedelta


def calculate_start_times(input_file: Path) -> None:
    estimated_times = []
    with open(input_file, "r") as f:
        for line in f.readlines():
            estimated_times.append(line)

    times = []

    for estimated_time in estimated_times:
        name, time_str = map(str, estimated_time.split(" - "))
        minutes, seconds = map(int, time_str.split(":"))
        times.append((name, timedelta(minutes=minutes, seconds=seconds)))

    sorted_times = sorted(times, key=lambda x: x[1], reverse=True)

    race_start_time = timedelta(hours=12)

    start_times: list[tuple] = []

    start_times.append((sorted_times[0][0], race_start_time))

    for time in sorted_times[1:]:
        start_times.append((time[0], race_start_time + (sorted_times[0][1] - time[1])))

    for start_time in start_times:
        print(f"{start_time[0]} - {start_time[1]}")


if __name__ == "__main__":
    from argparse import ArgumentParser, Namespace

    parser: ArgumentParser = ArgumentParser(
                    prog='Handicap race planner',
                    description='Plan a handicap race')

    parser.add_argument("--times", required=True, type=Path, help="Path to the file with predicted times")

    args: Namespace = parser.parse_args()

    if not args.times.is_file():
        exit(f"File does not exist: {args.times}")

    calculate_start_times(args.times)
