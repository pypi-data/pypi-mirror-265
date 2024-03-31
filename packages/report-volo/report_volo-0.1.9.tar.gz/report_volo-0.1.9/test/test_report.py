from argparse import Namespace
from src.report_volo.report import Record
import pytest
from datetime import datetime
import pathlib
import subprocess


@pytest.fixture
def mock_data_dir(tmp_path: pathlib.Path):
    """
    Creates a temporary directory with mock files for testing
    """
    mock_dir = tmp_path  # No need to create a subdirectory

    (mock_dir / "abbreviations.txt").write_text(
        "CLS_Charles Leclerc_SAUBER FERRARI\nLHM_Lewis Hamilton_MERCEDES\nDRR_Daniel Ricciardo_RED BULL RACING TAG HEUER\nABC\n1233@@abc"
    )
    (mock_dir / "start.log").write_text(
        "CLS2018-05-24_11:10:54.750\nLHM2018-05-24_12:10:32.585\nAHM2018-05-24_12:10:32.585\n_____\nDRR2018-05-24_12:14:12.054\n"
    )
    (mock_dir / "end.log").write_text(
        "CLS2018-05-24_12:10:54.750\nLHM2018-05-24_12:11:32.585\nAHM2018-05-24_12:11:32.585\n_____\nDRR2018-05-24_12:11:24.067"
    )

    return mock_dir


@pytest.mark.usefixtures("mock_data_dir")
def test_read_abbr(mock_data_dir):
    folder_path = mock_data_dir
    records_dict = {}
    abbr_file = "abbreviations.txt"

    output = Record.read_abbr(folder_path, records_dict, abbr_file)

    expected_data = [
        ("CLS", "Charles Leclerc", "SAUBER FERRARI"),
        ("LHM", "Lewis Hamilton", "MERCEDES"),
        ("DRR", "Daniel Ricciardo", "RED BULL RACING TAG HEUER"),
    ]

    for abbr, driver, team in expected_data:
        assert abbr in output
        assert output[abbr].driver == driver
        assert output[abbr].team == team

    assert "Bad data: abbreviations.txt, line: 4" in output
    assert "Bad data: abbreviations.txt, line: 5" in output


@pytest.mark.usefixtures("mock_data_dir")
def test_read_logs(mock_data_dir):
    folder_path = mock_data_dir

    mock_records_dict = {
        "CLS": Record(),
        "LHM": Record(),
        "DRR": Record(),
    }

    output_dict = Record.read_logs(
        folder_path, mock_records_dict, start_file="start.log", end_file="end.log"
    )

    expected_valid_cases = {
        "CLS": Record(
            start=datetime(2018, 5, 24, 11, 10, 54, 750000),
            end=datetime(2018, 5, 24, 12, 10, 54, 750000),
            error=None,
        ),
        "LHM": Record(
            start=datetime(2018, 5, 24, 12, 10, 32, 585000),
            end=datetime(2018, 5, 24, 12, 11, 32, 585000),
            error=None,
        ),
        "DRR": Record(
            start=datetime(2018, 5, 24, 12, 14, 12, 54000),
            end=None,
            error="Invalid end time: must be after the start time",
        ),
    }

    expected_invalid_cases = {
        "Bad line: 4, file: start": Record(
            None, None, None, None, None, "Bad line: 4, file: start"
        ),
        "Bad data: start, line: 5": Record(
            None, None, None, None, None, "Bad data: start, line: 5"
        ),
        "Bad line: 4, file: end": Record(
            None, None, None, None, None, "Bad line: 4, file: end"
        ),
        "Bad data: end, line: 5": Record(
            None, None, None, None, None, "Bad data: end, line: 5"
        ),
    }

    for record_key, expected_record in expected_valid_cases.items():
        assert output_dict[record_key] == expected_record

    for error_key, expected_error_record in expected_invalid_cases.items():
        assert output_dict[error_key].error == expected_error_record.error


@pytest.mark.usefixtures("mock_data_dir")
def test_build_report(mock_data_dir):
    folder_path = mock_data_dir

    # Expected Cases
    expected_good_records_asc = [
        Record(
            driver="Lewis Hamilton",
            team="MERCEDES",
            start=datetime(2018, 5, 24, 12, 10, 32, 585000),
            end=datetime(2018, 5, 24, 12, 11, 32, 585000),
            error=None,
            abbr="LHM",
        ),
        Record(
            driver="Charles Leclerc",
            team="SAUBER FERRARI",
            start=datetime(2018, 5, 24, 11, 10, 54, 750000),
            end=datetime(2018, 5, 24, 12, 10, 54, 750000),
            error=None,
            abbr="CLS",
        ),
    ]

    # Corrected Expected Good Records in Descending Order
    expected_good_records_desc = [
        Record(
            driver="Charles Leclerc",
            team="SAUBER FERRARI",
            start=datetime(2018, 5, 24, 11, 10, 54, 750000),
            end=datetime(2018, 5, 24, 12, 10, 54, 750000),
            error=None,
            abbr="CLS",
        ),
        Record(
            driver="Lewis Hamilton",
            team="MERCEDES",
            start=datetime(2018, 5, 24, 12, 10, 32, 585000),
            end=datetime(2018, 5, 24, 12, 11, 32, 585000),
            error=None,
            abbr="LHM",
        ),
    ]

    # Corrected Expected Bad Records
    expected_bad_records = [
        Record(
            driver="Daniel Ricciardo",
            team="RED BULL RACING TAG HEUER",
            start=datetime(2018, 5, 24, 12, 14, 12, 54000),
            end=None,
            error="Invalid end time: must be after the start time",
            abbr="DRR",
        ),
        Record(
            driver=None,
            team=None,
            start=None,
            end=None,
            error="Bad data: abbreviations.txt, line: 4",
            abbr=None,
        ),
        Record(
            driver=None,
            team=None,
            start=None,
            end=None,
            error="Bad data: abbreviations.txt, line: 5",
            abbr=None,
        ),
        Record(
            driver=None,
            team=None,
            start=None,
            end=None,
            error="Bad line: 4, file: start",
            abbr=None,
        ),
        Record(
            driver=None,
            team=None,
            start=None,
            end=None,
            error="Bad data: start, line: 5",
            abbr=None,
        ),
        Record(
            driver=None,
            team=None,
            start=None,
            end=None,
            error="Bad line: 4, file: end",
            abbr=None,
        ),
        Record(
            driver=None,
            team=None,
            start=None,
            end=None,
            error="Bad data: end, line: 5",
            abbr=None,
        ),
    ]

    # Test Case 1: Ascending Order
    good_records_asc, bad_records = Record.build_report(path=folder_path, order="asc")

    assert good_records_asc == expected_good_records_asc
    assert bad_records == expected_bad_records

    # Test Case 2: Descending Order
    good_records_desc, bad_records = Record.build_report(path=folder_path, order="desc")

    assert good_records_desc == expected_good_records_desc
    assert bad_records == expected_bad_records

    # Test Case 3: Invalid Order
    good_records_error, bad_records_error = Record.build_report(
        path=folder_path, order="error"
    )

    assert good_records_error == []
    assert bad_records_error == []


def test_print_report():
    expected_good_records_asc = [
        Record(
            driver="Lewis Hamilton",
            team="MERCEDES",
            start=datetime(2018, 5, 24, 12, 10, 32, 585000),
            end=datetime(2018, 5, 24, 12, 11, 32, 585000),
            error=None,
        ),
        Record(
            driver="Charles Leclerc",
            team="SAUBER FERRARI",
            start=datetime(2018, 5, 24, 11, 10, 54, 750000),
            end=datetime(2018, 5, 24, 12, 10, 54, 750000),
            error=None,
        ),
    ]

    expected_bad_records = [
        Record(
            driver="Daniel Ricciardo",
            team="RED BULL RACING TAG HEUER",
            start=datetime(2018, 5, 24, 12, 14, 12, 54000),
            end=None,
            error="Invalid end time: must be after the start time",
        ),
        Record(
            driver=None,
            team=None,
            start=None,
            end=None,
            error="Bad data: abbreviations.txt, line: 4",
        ),
        Record(
            driver=None,
            team=None,
            start=None,
            end=None,
            error="Bad data: abbreviations.txt, line: 5",
        ),
        Record(
            driver=None,
            team=None,
            start=None,
            end=None,
            error="Bad abbr: AHM, line: 3, file: start.log",
        ),
        Record(
            driver=None,
            team=None,
            start=None,
            end=None,
            error="Bad data: start.log, line: 4",
        ),
    ]

    print_report = Record.print_report(
        expected_good_records_asc, expected_bad_records, border_line=2
    )

    assert (
        print_report
        == """ 1. Lewis Hamilton       | MERCEDES                       | 0:01:00
 2. Charles Leclerc      | SAUBER FERRARI                 | 1:00:00
---------------------------------------------------------------------------
 3. Daniel Ricciardo     | RED BULL RACING TAG HEUER      | Invalid end time: must be after the start time
 4. Missing Data         | Missing Data                   | Bad data: abbreviations.txt, line: 4
 5. Missing Data         | Missing Data                   | Bad data: abbreviations.txt, line: 5
 6. Missing Data         | Missing Data                   | Bad abbr: AHM, line: 3, file: start.log
 7. Missing Data         | Missing Data                   | Bad data: start.log, line: 4
"""
    )


@pytest.mark.usefixtures("mock_data_dir")
def test_cli(mock_data_dir):
    dir_path = str(mock_data_dir)

    args_list = [
        ["--files", dir_path, "--asc"],
        ["--files", dir_path, "--desc"],
        ["--files", dir_path, "--asc", "--driver", "John Doe"],
    ]

    expected_outputs = [
        Namespace(files=dir_path, asc=True, desc=False, driver=None, sort="asc"),
        Namespace(files=dir_path, asc=False, desc=True, driver=None, sort="desc"),
        Namespace(files=dir_path, asc=True, desc=False, driver="John Doe", sort="asc"),
    ]

    outputs = []

    for args in args_list:
        output = Record.cli(args)
        outputs.append(output)
        print

    for output, expected_output in zip(outputs, expected_outputs):
        assert output == expected_output


if __name__ == "__main__":
    pytest.main([f"{__file__}", "-rx", "-vv"])
