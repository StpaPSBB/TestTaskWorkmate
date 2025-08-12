import pytest
from main import parse_args, read_logs_from_files, process_logs_average
from json import JSONDecodeError


def test_parse_args_file_provided(monkeypatch):
    """
    Tests correct parse_args function call.
    """
    monkeypatch.setattr("sys.argv",
                        ["main.py",
                         "--file", "test.log",
                         "--report", "average",
                         "--date", "2025-05-05"])
    args = parse_args()
    assert args.file == ["test.log"]
    assert args.report == "average"
    assert args.date == "2025-05-05"


def test_parse_args_wrong_report(monkeypatch):
    monkeypatch.setattr("sys.argv",
                        ["main.py",
                         "--file", "test.log",
                         "--report", "wrong_report",
                         "--date", "2025-05-05"])
    with pytest.raises(SystemExit):
        parse_args()


def test_parse_args_wrong_date(monkeypatch):
    """
    Tests wrong parse_args function call.
    """
    monkeypatch.setattr("sys.argv",
                        ["main.py",
                         "--file", "test.log",
                         "--report", "average",
                         "--date", "wrong_date"])
    with pytest.raises(SystemExit):
        parse_args()


def test_read_logs_from_files(tmp_path):
    """
    Tests correct read_logs_from_files function call.
    """
    file_path = tmp_path / "file.log"
    f = open(file_path, "w")
    f.write('{"@timestamp": "2025-06-22T13:57:32+00:00", \
             "status": 200, "url": "/api/test/...", \
             "request_method": "GET", "response_time": 0.024, \
             "http_user_agent": "..."}\n \
            {"@timestamp": "2025-06-22T13:57:32+00:00", \
             "status": 200, "url": "/api/test/...", \
             "request_method": "GET", "response_time": 0.02, \
             "http_user_agent": "..."}\n')
    f.close()
    logs = read_logs_from_files([str(file_path)])
    assert logs[0]["url"] == "/api/test/..."
    assert len(logs) == 2


def test_read_logs_file_not_found():
    """
    Tests FileNotFoundError call in wrong read_logs_from_files function call.
    """
    with pytest.raises(FileNotFoundError) as excinfo:
        read_logs_from_files(["missing_file"])
    assert "File not found: missing_file" in str(excinfo.value)


def test_read_logs_json_error(tmp_path):
    """
    Tests JSONDecodeError call in wrong read_logs_from_files function call.
    """
    broken_file_path = tmp_path / "broken_file.log"
    f = open(broken_file_path, 'w')
    f.write('{"url": "/test", "response_time": 0.1\n')
    f.close()
    with pytest.raises(JSONDecodeError) as excinfo:
        read_logs_from_files([str(broken_file_path)])
    assert (
        f"Invalid JSON in file {broken_file_path}: Expecting" in str(excinfo.value)
        )


def test_process_logs_average():
    """
    Tests correct process_logs_average function call.
    """
    logs = [
        {
            "@timestamp": "2025-06-22T13:57:32+00:00",
            "status": 200,
            "url": "/api/test1/...",
            "request_method": "GET",
            "response_time": 0.1,
            "http_user_agent": "..."
        },
        {
            "@timestamp": "2025-06-22T13:57:32+00:00",
            "status": 200,
            "url": "/api/test1/...",
            "request_method": "GET",
            "response_time": 0.2,
            "http_user_agent": "..."
        },
        {
            "@timestamp": "2025-06-22T13:57:32+00:00",
            "status": 200, "url": "/api/test2/...",
            "request_method": "GET",
            "response_time": 0.3,
            "http_user_agent": "..."
        },
        {
            "@timestamp": "2025-06-22T13:57:32+00:00",
            "status": 200,
            "url": "/api/test3/...",
            "request_method": "GET",
            "response_time": 0.4,
            "http_user_agent": "..."
        }
    ]
    data = process_logs_average(logs)
    assert data[0][1] == "/api/test1/..."
    assert data[0][2] == 2
    assert data[0][3] == pytest.approx(0.15)
    assert len(data) == 3
