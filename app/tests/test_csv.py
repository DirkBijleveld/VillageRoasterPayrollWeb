from datetime import datetime
from pathlib import Path

import pandas as pd
from pandas import read_csv
from pytest import fixture
from pytest import mark

from app.csv.csv import (
    get_payroll_period,
    read_file,
    clean_blanks,
    clean_excess_headers,
    clean_empty_shifts,
    clean_types,
)

param = mark.parametrize


@fixture
def resource_dir() -> Path:
    return Path(__file__).parent / "resources"


@fixture
def csv_dir(resource_dir: Path) -> Path:
    return resource_dir / "csv"


@fixture
def csv_1_path(csv_dir: Path) -> Path:
    return csv_dir / "ts_feb_22.csv"


@fixture
def csv_2_path(csv_dir: Path) -> Path:
    return csv_dir / "ts_nov_21.csv"


@fixture
def df_1(csv_1_path: Path) -> pd.DataFrame:
    return pd.read_csv(csv_1_path, header=3)


@fixture
def df_2(csv_2_path: Path) -> pd.DataFrame:
    return pd.read_csv(csv_2_path, header=3)


# Tests
@param("csv_path", [csv_1_path, csv_2_path])
def test_read_file(csv_path: Path, request):
    csv_path = request.getfixturevalue(csv_path.__name__)
    assert csv_path.exists()
    df = read_file(csv_path)
    assert len(df["Name"]) > 0


@param("csv_path", [csv_1_path, csv_2_path])
def test_get_payroll_period(csv_path: Path, request):
    csv_path = request.getfixturevalue(csv_path.__name__)
    assert csv_path.exists()
    p1, p2 = get_payroll_period(csv_path)
    assert p1 < p2
    assert p1.year == p2.year


@param("df", [df_1, df_2])
def test_clean_blanks(df: pd.DataFrame, request):
    df = request.getfixturevalue(df.__name__)
    length_1 = len(df["Name"])
    assert length_1 > 0
    df = clean_blanks(df)
    length_2 = len(df["Name"])
    assert length_2 < length_1


@param("df", [df_1, df_2])
def test_clean_excess_headers(df: pd.DataFrame, request):
    df = request.getfixturevalue(df.__name__)
    length_1 = len(df["Name"])
    assert length_1 > 0
    df = clean_excess_headers(df)
    length_2 = len(df["Name"])
    assert length_2 < length_1


@param("df", [df_1, df_2])
def test_clean_empty_shifts(df: pd.DataFrame, request):
    df = request.getfixturevalue(df.__name__)
    length_1 = len(df["Name"])
    assert length_1 > 0
    df = clean_empty_shifts(df)
    length_2 = len(df["Name"])
    # Unlike other tests, I cannot assume there will always be empty shifts.
    assert length_2 <= length_1


@param("df", [df_1, df_2])
def test_clean_types(df: pd.DataFrame, request):
    df = request.getfixturevalue(df.__name__)
    df = clean_blanks(df)
    df = clean_excess_headers(df)
    df = clean_empty_shifts(df)
    df = clean_types(df)
    assert df["Name"].dtype == "string"
    assert df["Payroll ID"].dtype == "int64"
    assert df["Clock in datetime"].dtype == "datetime64[ns]"
    assert df["Clock out datetime"].dtype == "datetime64[ns]"
    assert df["Break start"].dtype == "datetime64[ns]"
    assert df["Break end"].dtype == "datetime64[ns]"
    assert df["Role"].dtype == "string"
    assert df["Wage"].dtype == "int64"
    assert df["Scheduled"].dtype == "int64"
    assert df["Issues"].dtype == "string"
    assert df["Employee Note"].dtype == "string"
    assert df["Manager Note"].dtype == "string"
    assert df["Break paid"].dtype == "bool"
