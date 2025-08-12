import argparse
import re
from typing import Any, Callable
from json import loads, JSONDecodeError
from tabulate import tabulate

REPORTS = {}


def reg_report(name: str) -> Callable[[Callable], Callable]:
    """
    Decorates function to register report name.
    """
    def decorator(func):
        REPORTS[name] = func
        return func
    return decorator


def validate_report(value: str) -> str:
    """
    Validates that report name is in the registered reports.
    """
    if value not in REPORTS:
        allowed = ", ".join(sorted(REPORTS.keys()))
        raise argparse.ArgumentTypeError(
            f"Invalid report name '{value}'. Allowed report names: {allowed}"
            )
    else:
        return value


def validate_date(pattern: str) -> Callable[[str], str]:
    """
    Creates a validator for date based on pattern.
    """
    def validator(value: str) -> str:
        """
        Validates date based on pattern.
        """
        if not re.fullmatch(pattern, value):
            raise argparse.ArgumentTypeError(
                f"{value} not in pattern: 2025-06-22"
                )
        else:
            return value
    return validator


def parse_args():
    """
    Parses command-line arguments for the script.
    """
    parser = argparse.ArgumentParser(description="Report scrip")
    parser.add_argument("--file",
                        dest="file",
                        nargs="+",
                        required=True)
    parser.add_argument("--report",
                        dest="report",
                        type=validate_report,
                        required=True)
    parser.add_argument("--date",
                        dest="date",
                        type=validate_date(r"\d{4}-\d{2}-\d{2}"))
    return parser.parse_args()


def read_logs_from_files(files: list[str]) -> list[dict[str, Any]]:
    """
    Reads and parses JSON logs from log files.
    """
    logs = []
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        logs.append(loads(line))
        except JSONDecodeError as e:
            raise JSONDecodeError(
                f"Invalid JSON in file {file}: {str(e)}", e.doc, e.pos
                )
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file}")
    return logs


@reg_report("average")
def process_logs_average(logs: list[dict[str, Any]],
                         date_filter: str = None) -> list[tuple[int, str, int, float]]:
    """
    Processes logs.
    Creates report data.
    """
    endpoints = {}
    for log in logs:
        url = log["url"]
        response_time = log["response_time"]
        if date_filter is not None:
            log_date = log["@timestamp"][:10]
            if log_date != date_filter:
                continue
        if url in endpoints:
            endpoints[url]["total"] += 1
            endpoints[url]["total_response_time"] += response_time
        else:
            endpoints[url] = {"total": 1, "total_response_time": response_time}
    data = []
    n = 0
    for k, v in endpoints.items():
        avg_response_time = v["total_response_time"]/v["total"]
        data.append((n, k, v["total"], round(avg_response_time, 4)))
        n += 1
    return data


def print_table(data: list[tuple], columns: list[str]):
    """
    Draws a table.
    """
    print(tabulate(data, headers=columns))


if __name__ == "__main__":
    try:
        args = parse_args()
        logs = read_logs_from_files(args.file)
        process_logs_report_func = REPORTS[args.report]
        data = process_logs_report_func(logs, args.date)
        print_table(data,
                    columns=['', 'handler', 'total', 'avg_response_time'])
    except Exception as e:
        print(f"Error: {e}")
