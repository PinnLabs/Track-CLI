import re
import sys
from datetime import datetime, timedelta
from io import StringIO
from unittest.mock import patch

import pytest

from timecli import report


@patch("timecli.report.load_sessions")
def test_generate_report_multiple_sessions_same_project(mock_load):
    now = datetime.now()
    mock_load.return_value = [
        {
            "project": "Project X",
            "tags": ["t1"],
            "start": (now - timedelta(minutes=30)).isoformat(),
            "end": now.isoformat(),
        },
        {
            "project": "Project X",
            "tags": ["t2"],
            "start": (now - timedelta(minutes=20)).isoformat(),
            "end": now.isoformat(),
        },
    ]

    captured_output = StringIO()
    sys.stdout = captured_output
    report.generate_report()
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "- Project X:" in output
    minutes = re.findall(r"- Project X: ([\d\.]+) minutes", output)
    assert minutes
    total_minutes = float(minutes[0])
    assert 48 <= total_minutes <= 52


@patch("timecli.report.load_sessions")
def test_generate_report_with_invalid_date(mock_load):
    mock_load.return_value = [
        {
            "project": "Project Y",
            "tags": [],
            "start": "invalid-date",
            "end": datetime.now().isoformat(),
        }
    ]

    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        report.generate_report()
    except Exception as e:
        pytest.fail(f"generate_report raised exception with invalid date: {e}")
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "Project Y" not in output


@patch("timecli.report.load_sessions")
def test_generate_report_empty_sessions(mock_load):
    mock_load.return_value = []

    captured_output = StringIO()
    sys.stdout = captured_output
    report.generate_report()
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "Report" in output
    assert "-" not in output


@patch("timecli.report.load_sessions")
def test_show_log_missing_fields(mock_load):
    now = datetime.now()
    mock_load.return_value = [
        {"project": "Project Z", "start": now.isoformat()},
    ]

    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        report.show_log()
    except Exception as e:
        pytest.fail(f"show_log raised exception on missing fields: {e}")
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "Project Z" in output
    assert "In progress" in output


@patch("timecli.report.load_sessions")
def test_show_log_empty_sessions(mock_load):
    mock_load.return_value = []

    captured_output = StringIO()
    sys.stdout = captured_output
    report.show_log()
    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert output.strip() == ""
