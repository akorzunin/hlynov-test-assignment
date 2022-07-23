import pytest
import os
import sys
sys.path.insert(1, r'C:\Users\akorz\Documents\hlynov-test-assignment')
# from src.xml_file_parser import XmlFileParser
from main import app

def collect_paths_to_test_files() -> dict[str, list]:
    '''Read content of folder w/ test files and return paths to test files'''
    abs_file_paths = []
    rel_file_paths = []
    for root, dirs, files in os.walk('./test/test_files'):
        for file in files:
            file_path = f'{root}/{file}'
            rel_file_paths.append(file_path)
            abs_file_paths.append(
                os.path.abspath(file_path)
            )
    return dict(
        abs_file_paths=abs_file_paths,
        rel_file_paths=rel_file_paths,
    )

test_files = collect_paths_to_test_files()


@pytest.fixture
def parser(valid_file_path):
    '''Create parser object'''
    return app.parse_file(
        file_path=valid_file_path
    )

@pytest.mark.parametrize(
    "file_path",
    [
        *test_files['rel_file_paths'],
        *test_files['abs_file_paths'],
    ]
)
def test_valid_file_path(file_path) -> None:
    assert app.parse_file(
        file_path=file_path,
    )

### questionable tests
def test_output_encoding() -> None:
    ...

def test_csv_dlim() -> None:
    ...

def test_logs_exists() -> None:
    ...

def test_cli_run() -> None:
    ...

def test_csv_output_loc() -> None:
    ...

def test_xml_input_loc() -> None:
    ...


def test_csv_fields() -> None:
    ...

def test_duplicates() -> None:
    '''csv output should not contain duplicates'''
    # len csv file == set(csv_file)
    ...

def test_csv_field_validation() -> None:
    # mb use pydantic to validate all csv rows as models
    ...

def test_bad_xml_input_loc() -> None:
    ...

### over tests
def test_not_key_field_missing() -> None:
    # handle missing key as blank field
    ...

def test_key_field_missing() -> None:
    # skip row
    ...

