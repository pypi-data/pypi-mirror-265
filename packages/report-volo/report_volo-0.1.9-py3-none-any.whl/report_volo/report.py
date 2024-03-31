import re
import copy
import argparse
from pathlib import Path
from datetime import datetime, timedelta


class FileNotFound(Exception):
    pass


class ReportInvalidOrder(Exception):
    pass


class Record:
    regex_abbr = re.compile(r"(^[A-Z]{3})_(\w+\s\w+)_([A-Z\s]+$)")
    regex_log = re.compile(r"(^[A-Z]{3})(\d+-\d+-\d+_\d+:\d+:\d+.\d+)")

    def __init__(
        self,
        abbr: str = None,
        driver: str = None,
        team: str = None,
        start: datetime = None,
        end: datetime = None,
        error: str = None,
    ):
        self.abbr = abbr
        self.driver = driver
        self.team = team
        self._start = start
        self._end = end
        self.error = error

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if isinstance(value, datetime):
            if not self.end or self.end > value:
                self._start = value
            else:
                self.error = "Invalid start time: must be before the end time"
        else:
            self.error = "start() expects a datetime object"

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        if isinstance(value, datetime):
            if not self.start or self.start < value:
                self._end = value
            else:
                self.error = "Invalid end time: must be after the start time"
        else:
            self.error = "end() expects a datetime object"

    @property
    def result(self):
        return self.end - self.start if self.start and self.end else None

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Record):
            return (
                self.abbr == value.abbr
                and self.team == value.team
                and self.driver == value.driver
                and self._end == value.end
                and self._start == value.start
                and self.error == value.error
            )
        else:
            return NotImplemented

    def __ne__(self, value: object) -> bool:
        x = self.__eq__(value)
        return not x if x is not NotImplemented else NotImplemented

    def __repr__(self):
        return f"Record({self.abbr}, {self.driver}, {self.team}, {self.start}, {self.end}, {self.error})"

    @classmethod
    def dict_init(cls, records_dict: dict[str, "Record"] = None) -> dict[str, "Record"]:
        """
        Initialize a dictionary for use in the read_abbr and read_logs methods.

        Args:
            records_dict (dict[str, Record], optional): Dictionary to initialize. Defaults to None.

        Returns:
            dict[str, Record]: Initialized dictionary or a deep copy of the input dictionary.
        """
        records_dict_copy = copy.deepcopy(
            records_dict if records_dict is not None else {}
        )
        return records_dict_copy

    @classmethod
    def read_file(cls, path: str | Path, insert_file: str) -> list[str]:
        """
        Validate the file path, read the file, and remove leading and trailing whitespace
        characters from every line in the file.

        Args:
            path (str or Path): Directory path containing the file.
            insert_file (str): Name of the file to read.

        Returns:
            list[str]: List of lines from the file with leading and trailing whitespace removed.
        """
        file_path = Path(path) / insert_file
        if not file_path.exists():
            raise FileNotFound(f"{file_path} not found")

        lines_list = [line.strip() for line in open(file_path, "r")]

        return lines_list

    @classmethod
    def read_abbr(
        cls,
        path: str | Path,
        records_dict: dict[str, "Record"] = None,
        abbr_file: str = "abbreviations.txt",
    ) -> dict[str, "Record"]:
        """
        Extract abbreviations from a file and save them in a deep
        copy of the data dictionary, retaining only lines that match the regular expression pattern.

        Args:
            path (str or Path): Directory path containing the abbreviation file.
            records_dict (dict[str, Record], optional): Dictionary to store parsed records. Defaults to None.
            abbr_file (str, optional): Name of the abbreviation file. Defaults to "abbreviations.txt".

        Returns:
            dict[str, Record]: Dictionary containing parsed abbreviation data.

        Raises:
            FileNotFound: If the specified abbreviation file is not found.
        """
        records_dict_copy = cls.dict_init(records_dict)

        lines_list = cls.read_file(path, abbr_file)
        for line_index, line in enumerate(lines_list, start=1):
            if cls.regex_abbr.match(line):
                abbr, driver, team = line.split("_")
                record = cls()
                setattr(record, "abbr", abbr)
                setattr(record, "driver", driver)
                setattr(record, "team", team)
                records_dict_copy[abbr] = record
            else:
                abbr_error = f"Bad data: {abbr_file}, line: {line_index}"
                records_dict_copy[abbr_error] = cls(error=abbr_error)

        return records_dict_copy

    @classmethod
    def file_name(cls, insert_file):
        """
        Determine log type based on file name. Used in read_data method to assing log's to relevant attributes.

        Args:
            insert_file (str): File name to analyze.

        Returns:
            str or False: Log type ("start" or "end") if recognized, else False.
        """
        return (
            "start"
            if insert_file == "start.log"
            else ("end" if insert_file == "end.log" else False)
        )

    @classmethod
    def read_data(
        cls,
        path: str | Path,
        insert_file: str,
        records_dict: dict[str, "Record"] = None,
    ) -> dict[str, "Record"]:
        """
        Read and parse log data from a file.

        Args:
            path (str or Path): Directory path containing log files.
            insert_file (str): Name of the log file to read.
            records_dict (dict[str, Record], optional): Dictionary for parsed records. Defaults to None.

        Returns:
            dict[str, Record]: Parsed log data dictionary.

        Raises:
            FileNotFoundError: If the log file is not found.
        """
        records_dict_copy = cls.dict_init(records_dict)
        file_name = cls.file_name(insert_file)

        file_path = Path(path) / insert_file
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} not found")

        with open(file_path, "r") as file:
            for line_index, line in enumerate(file, start=1):
                if match := cls.regex_log.match(line.strip()):
                    record_key, log_time = match.groups()
                    record = records_dict_copy.get(record_key, cls())
                    setattr(record, file_name, datetime.fromisoformat(log_time))
                else:
                    log_error = f"Bad line: {line_index}, file: {file_name}"
                    records_dict_copy[log_error] = cls(error=log_error)
            else:
                log_error = f"Bad data: {file_name}, line: {line_index}"
                records_dict_copy[log_error] = cls(error=log_error)

        return records_dict_copy

    @classmethod
    def read_logs(
        cls,
        path: str | Path,
        records_dict: dict[str, "Record"] = None,
        start_file: str = "start.log",
        end_file: str = "end.log",
    ) -> dict[str, "Record"]:
        """
        Read and parse start and end log files into a record dictionary.

        Args:
            path (str or Path): Directory path containing log files.
            records_dict (dict[str, Record], optional): Dictionary for parsed records. Defaults to None.
            start_file (str, optional): Name of the start log file. Defaults to "start.log".
            end_file (str, optional): Name of the end log file. Defaults to "end.log".

        Returns:
            dict[str, Record]: Parsed start and end log data dictionary.

        Raises:
            FileNotFoundError: If start or end log file is not found.
        """
        records_dict_copy = cls.dict_init(records_dict)

        start_dict = cls.read_data(path, start_file, records_dict_copy)
        full_dict = cls.read_data(path, end_file, start_dict)

        return full_dict

    @classmethod
    def build_report(
        cls,
        path: str | Path,
        order: str = "asc",
    ) -> tuple[list["Record"], list["Record"]]:
        """
        Compiles a report summarizing valid and invalid records based on provided logs and abbreviations.

        Reads log files (end.log and start.log), parses abbreviations from a text file (abbreviations.txt).
        Validates the order operator and sorts the data in ascending or descending order.

        Args:
            path: Path to the directory containing the log files and abbreviations text file.
            order: Sort order for records, 'asc' (ascending) or 'desc' (descending). Defaults to 'asc'.

        Returns:
            Tuple with two lists: good_record as valid list and bad_records as list of broken records.
        """
        good_records, bad_records = [], []

        try:
            if order not in ["asc", "desc"]:
                raise ReportInvalidOrder(
                    f"Invalid sorting order '{order}'. Valid options are: asc, desc"
                )

            records_dict = Record.read_abbr(path=path)
            records_dict = Record.read_logs(path=path, records_dict=records_dict)

            for rec in records_dict.values():
                (bad_records if rec.error else good_records).append(rec)

            multiplier = 1 if order == "asc" else -1
            good_records.sort(key=lambda x: multiplier * (x.result or timedelta(0)))

        except ReportInvalidOrder as e:
            print(str(e))
            return [], []

        return good_records, bad_records

    @classmethod
    def print_report(cls, good_records, bad_records, border_line: int = 15):
        """
        Print a formatted report based on a list of ordered results.

        Args:
            good_records - list of valid records in dict
            bad_records - list of invalid records in dict
        """
        result_string = ""
        line_count = 0

        for num, rec in enumerate(good_records + bad_records, start=1):
            driver = rec.driver if rec.driver is not None else "Missing Data"
            team = rec.team if rec.team is not None else "Missing Data"
            abbr = rec.abbr if rec.abbr is not None else "Missing Data"
            result = rec.result if not rec.error else rec.error

            record_str = f"{num:2}. {driver:<20} | {team:<30} | {result}"

            result_string += record_str + "\n"

            if num == border_line:
                result_string += "-" * 75 + "\n"
            line_count += 1

        return result_string

    @classmethod
    def cli(cls, args_list=None) -> argparse.Namespace:
        """
        Parses command-line arguments and orchestrates the report generation process.

        Args:
            args_list (list): List of strings representing command-line arguments.

        Returns:
            argparse.Namespace: Parsed command-line arguments.

        Example:
            Record.cli(["--files", "../data", "--asc", "--driver", "Sergey Sirotkin"])
        """
        parser = argparse.ArgumentParser(description="Build Monaco report")

        parser.add_argument("--files", required=True, help="Path to folder")

        group = parser.add_mutually_exclusive_group()
        group.add_argument("--asc", action="store_true", help="Ascending order sort")
        group.add_argument("--desc", action="store_true", help="Descending order sort")
        parser.add_argument("--driver", help="Show statistics for a specific driver")

        args = parser.parse_args(args_list)
        print(args)

        args.sort = "asc" if args.asc else "desc"

        good_records, bad_records = [], [] 

        if args.driver:
            good_records = [rec for rec in good_records if rec.driver == args.driver]
            bad_records = [rec for rec in bad_records if rec.driver == args.driver]

        return args


if __name__ == "__main__":
    args = Record.cli()
    good_records, bad_records = Record.build_report(args.files, args.sort)
    print(Record.print_report(good_records, bad_records))
