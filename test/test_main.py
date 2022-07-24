import chardet
import pytest
import pandas as pd
import os
import sys
import subprocess

PWD = os.path.abspath(os.getcwd())
sys.path.insert(1, PWD)

from main import app
from src.validation import col_descriptions


def collect_paths_to_test_files(dir_path: str, extension: str) -> dict[str, list]:
    '''Read content of folder w/ test files and return paths to test files'''
    abs_file_paths = []
    rel_file_paths = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # add only xml files
            if os.path.splitext(file)[-1] == extension:
                file_path = f'{root}/{file}'
                rel_file_paths.append(file_path)
                abs_file_paths.append(
                    os.path.abspath(file_path)
                )
    return dict(
        abs_file_paths=abs_file_paths,
        rel_file_paths=rel_file_paths,
    )

test_files = collect_paths_to_test_files(
    dir_path='./test/test_files', 
    extension='.xml',
)
bad_test_files = collect_paths_to_test_files(
    dir_path='./test/test_bad_files', 
    extension='.test',
)


file_paths = pytest.mark.parametrize(
    "file_path",
    [
        *test_files['rel_file_paths'],
        *test_files['abs_file_paths'],
    ]
)
bad_file_paths = pytest.mark.parametrize(
    "bad_file_path",
    [
        *bad_test_files['rel_file_paths'],
        # *bad_test_files['abs_file_paths'],
    ]
)

def move_bad_file_back(file_path: str):
    os.replace(
        os.path.join(
            os.path.dirname(file_path),
            'bad',
            os.path.basename(file_path)
        ),
        file_path, 
    )

@pytest.fixture
def parser():
    '''Create parser object'''
    return app

@pytest.fixture
def output() -> list:
    '''Get path to pased file'''
    return app.parse_file(
        file_path=test_files['abs_file_paths'][0]
    ), app

@file_paths
def test_valid_file_path(file_path: str) -> None:
    assert app.parse_file(
        file_path=file_path,
    )

@file_paths
def test_output_encoding(file_path: str) -> None:
    '''detect encoding of output file'''
    parsed_file_path = app.parse_file(
        file_path=file_path,
    )
    with open(parsed_file_path, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(10000))
        assert result['encoding'] == app.encoding

def test_csv_dlim(output: list) -> None:
    '''Check delimiter of output file'''
    output_file_path, app = output
    df = pd.read_csv(
        filepath_or_buffer=output_file_path,
        delimiter=';',
        header=None,
        names=col_descriptions.values(),
        encoding=app.encoding,
    )
    assert len(df.columns) > 1 and len(df)
    
def test_logs_exists(output: list) -> None:
    output_file_path, app = output
    folder = os.path.dirname(output_file_path)
    assert os.path.isfile(folder+'/log/parser.log')

@file_paths
def test_cli_run(file_path: str) -> None:
    '''Run program w/ test_files as input'''
    process = subprocess.run(["python", "main.py", file_path])
    assert not process.returncode

# TODO cant use output fixture here
def test_csv_output_loc(output: list) -> None:
    '''csv file must be in same directory as input file and have same name'''
    output_file_path, app = output
    get_name = lambda path: os.path.splitext(os.path.basename(path))[0]
    get_folder = lambda path: os.path.dirname(path)
    assert get_name(output_file_path) == get_name(app.file_path)
    assert get_folder(output_file_path) == get_folder(app.file_path)

@pytest.mark.skip('cant move files rn')
def test_xml_input_loc(output: list) -> None:
    '''move valid xml to /arh folder\n
    move invalid xml to /bad folder
    '''
    output_file_path, app = output
    base = os.path.basename(app.file_path)
    folder = os.path.dirname(app.file_path)
    assert os.path.isfile(os.path.join(folder, 'arh', base)) or\
        os.path.isfile(os.path.join(folder, 'bad', base))

def test_csv_fields(output: list) -> None:
    output_file_path, app = output
    df = pd.read_csv(
        filepath_or_buffer=output_file_path,
        delimiter=';',
        header=None,
        names=col_descriptions.values(),
        encoding=app.encoding,
    )
    # TODO refactor this test
    assert len(df.columns) == len(col_descriptions)

def test_duplicates(output: list) -> None:
    '''csv output should not contain duplicates of fiels personal_account and period'''
    output_file_path, app = output
    df = pd.read_csv(
        filepath_or_buffer=output_file_path,
        delimiter=';',
        header=None,
        names=col_descriptions.values(),
        encoding=app.encoding,
    )
    df.columns = col_descriptions.values()
    assert not df.duplicated(
        subset=[
            col_descriptions['personal_account'],
            col_descriptions['period']
        ],
    ).any()

# TODO validation
def test_csv_field_validation() -> None:
    # mb use pydantic to validate all csv rows as models
    ...

def test_not_key_field_missing() -> None:
    # handle missing key as blank field
    ...

def test_key_field_missing() -> None:
    # skip row
    ...

