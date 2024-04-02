import csv
import json
import pathlib
import yaml
from typing import List, OrderedDict
from warnings import warn


def from_csv(
    filepath: pathlib.Path | str,
    encoding: str = "utf-8",
    newline: str = "",
    delimiter: str = ",",
) -> List[list]:
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list of lists,
    wherein each nested list represents a single row from the input file.

    WARN: If a byte order mark (BOM) is encountered at the beginning of the first line of decoded
    text, call < from_csv > and pass 'utf-8-sig' as the < encoding > argument.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
    may not be interpreted correctly by the csv.reader.

    Parameters:
        filepath (pathlib.Path | str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: a list of nested "row" lists
    """

    with open(filepath, "r", encoding=encoding, newline=newline) as file_obj:
        return [row for row in csv.reader(file_obj, delimiter=delimiter)]


def from_csv_to_dicts(
    filepath: pathlib.Path | str,
    encoding: str = "utf-8",
    newline: str = "",
    delimiter: str = ",",
    ordered: bool = True,
) -> List[OrderedDict] | List[dict]:
    """Accepts a file path, creates a file object, and returns a list of dictionaries
    that represent the row values using the cvs.DictReader(). Default type returned
    in list is an OrderedDict which can be overridden.

    Parameters:
        filepath (pathlib.Path | str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values
        ordered (bool): return either list of OrderedDict objects or dict objects

    Returns:
        list: nested dictionaries representing the file contents
    """

    with open(filepath, "r", newline=newline, encoding=encoding) as file_obj:
        if ordered:
            return [row for row in csv.DictReader(file_obj, delimiter=delimiter)]
        else:
            return [dict(row) for row in csv.DictReader(file_obj, delimiter=delimiter)]


def from_json(filepath: pathlib.Path | str, encoding: str = "utf-8") -> dict | list:
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (pathlib.Path | str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict | list: dict or list representations of the decoded JSON document
    """

    with open(filepath, "r", encoding=encoding) as file_obj:
        return json.load(file_obj)


def from_txt(
    filepath: pathlib.Path | str, encoding: str = "utf-8", strip: bool = True
) -> List[str]:
    """Read text file line by line. Remove whitespace and trailing newline
    escape character.

    Parameters:
        filepath (pathlib.Path | str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file.
        strip (bool): remove white space, newline escape characters

    Returns
        list: list of lines in file
    """

    with open(filepath, "r", encoding=encoding) as file_obj:
        if strip:
            return [line.strip() for line in file_obj]
        else:
            return file_obj.readlines()


def from_yaml(filepath: pathlib.Path | str) -> dict | list:
    """Read a YAML (Yet Another Markup Language) file given a valid filepath.

    Parameters:
        filepath (pathlib.Path | str): absolute or relative path to source file

    Returns:
        dict | list: typically a list or dictionary representation of the file object
    """

    with open(filepath, "r") as file_object:
        return yaml.load(file_object, Loader=yaml.FullLoader)


def read_csv(
    filepath: pathlib.Path | str,
    encoding: str = "utf-8",
    newline: str = "",
    delimiter: str = ",",
) -> List[list]:
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list of lists,
    wherein each nested list represents a single row from the input file.

    WARN: If a byte order mark (BOM) is encountered at the beginning of the first line of decoded
    text, call < from_csv > and pass 'utf-8-sig' as the < encoding > argument.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
    may not be interpreted correctly by the csv.reader.

    Parameters:
        filepath (pathlib.Path | str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: a list of nested "row" lists
    """

    warn(
        "read_csv() is deprecated and will be removed from umpyutl 3.0.0. Use from_csv().",
        DeprecationWarning,
        stacklevel=2,
    )

    return from_csv(filepath, encoding, newline, delimiter)


def read_csv_to_dicts(
    filepath: pathlib.Path | str,
    encoding: str = "utf-8",
    newline: str = "",
    delimiter: str = ",",
    ordered: bool = True,
) -> List[OrderedDict] | List[dict]:
    """Accepts a file path, creates a file object, and returns a list of dictionaries
    that represent the row values using the cvs.DictReader(). Default type returned
    in list is an OrderedDict which can be overridden.

    Parameters:
        filepath (pathlib.Path | str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values
        ordered (bool): return either list of OrderedDict objects or dict objects

    Returns:
        list: nested dictionaries representing the file contents
    """

    warn(
        "read_csv_to_dicts() is deprecated and will be removed from umpyutl 3.0.0. Use from_csv_to_dicts().",
        DeprecationWarning,
        stacklevel=2,
    )

    return from_csv_to_dicts(filepath, encoding, newline, delimiter, ordered)


def read_file(
    filepath: pathlib.Path | str, encoding: str = "utf-8", strip: bool = True
) -> List[str]:
    """Read text file line by line. Remove whitespace and trailing newline
    escape character.

    Parameters:
        filepath (pathlib.Path | str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file.
        strip (bool): remove white space, newline escape characters

    Returns
        list: list of lines in file
    """

    warn(
        "read_file() is deprecated and will be removed from umpyutl 3.0.0. Use from_txt().",
        DeprecationWarning,
        stacklevel=2,
    )

    return from_txt(filepath, encoding, strip)


def read_json(filepath: pathlib.Path | str, encoding: str = "utf-8") -> dict | list:
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (pathlib.Path | str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict | list: dict or list representations of the decoded JSON document
    """

    warn(
        "read_file() is deprecated and will be removed from umpyutl 3.0.0. Use from_json().",
        DeprecationWarning,
        stacklevel=2,
    )

    return from_json(filepath, encoding)


def read_yaml(filepath: pathlib.Path | str) -> dict | list:
    """Read a YAML (Yet Another Markup Language) file given a valid filepath.

    Parameters:
        filepath (pathlib.Path | str): absolute or relative path to source file

    Returns:
        dict | list: typically a list or dictionary representation of the file object
    """

    warn(
        "read_yaml() is deprecated and will be removed from umpyutl 3.0.0. Use from_yaml().",
        DeprecationWarning,
        stacklevel=2,
    )

    return from_yaml(filepath)
