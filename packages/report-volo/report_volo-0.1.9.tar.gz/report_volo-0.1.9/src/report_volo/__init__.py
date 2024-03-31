from .report import Record, FileNotFound, ReportInvalidOrder


def read_abbr(path, records_dict=None, abbr_file="abbreviations.txt"):
    return Record.read_abbr(path, records_dict, abbr_file)


def read_logs(path, records_dict=None, start_file="start.log", end_file="end.log"):
    return Record.read_logs(path, records_dict, start_file, end_file)


def build_report(path, order="asc"):
    return Record.build_report(path, order)


def print_report(good_records, bad_records, border_line: int = 15):
    return Record.print_report(good_records, bad_records)


def cli(args_list=None):
    return Record.cli(args_list)


def record_report(args=None):
    return Record.record_report(args)


__all__ = [
    "FileNotFound",
    "ReportInvalidOrder",
    "Record",
    "cli",
    "build_report",
    "read_abbr",
    "read_logs",
    "print_report",
    "record_report",
]
