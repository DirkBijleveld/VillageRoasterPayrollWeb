from datetime import datetime
from decimal import Decimal
from typing import BinaryIO

import pandas as pd


def read_file(file: BinaryIO, header: int = 3) -> pd.DataFrame:
    return pd.read_csv(file, header=header)


def get_payroll_period(file: BinaryIO) -> tuple[datetime, datetime]:
    df = read_file(file, header=0)
    payroll_strings = df.iat[0, 1].split(" To ")
    return datetime.strptime(payroll_strings[0], "%m/%d/%Y"), datetime.strptime(
        payroll_strings[1], "%m/%d/%Y"
    )


# In order to run all functions dynamically (auto-add new functions to the list)
# We use a global list with a decorator.
# Lists are ordered by their nature, so we can run the functions in order.
CLEANING_FUNCTIONS = []


def cleaner(func: callable) -> callable:
    """
    Decorator to add a function to the CLEANING_FUNCTIONS list
    """
    global CLEANING_FUNCTIONS
    CLEANING_FUNCTIONS.append(func)
    return func


@cleaner
def clean_blanks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows that are blank or have a blank first column
    """
    first_col = df.columns[0]
    df[first_col] = df[first_col].fillna("-")
    df = df[
        ~(df[first_col] == "")
        & ~(df[first_col] == "-")
        & ~(df[first_col].str.startswith("Totals for "))
    ]
    return df


@cleaner
def clean_excess_headers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate header rows buried in .csv
    """
    first_col = df.columns[0]
    df = df[~(df[first_col] == first_col)]
    return df


@cleaner
def clean_empty_shifts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes shifts without a clock in time AND clock out time, AND removes shifts without a clock in date AND clock out date
    """
    df = df[
        ~(pd.isna(df["Clock in time"]) & pd.isna(df["Clock out time"]))
        & ~(pd.isna(df["Clock in date"]) & pd.isna(df["Clock out date"]))
    ]
    return df


def to_int(x, placeholder: int = 9999) -> int:
    try:
        return int(x)
    except ValueError:
        return placeholder


def to_str(x, placeholder: str = "") -> str:
    try:
        return str(x)
    except ValueError:
        return placeholder


def to_datetime(x: str) -> datetime | None:
    try:
        return datetime.strptime(x, "%m %B %Y%I:%M%p")
    except ValueError:
        return None


def to_currency(x: str) -> int:
    try:
        return int(Decimal(x.strip().strip("$").strip(",")) * 1000)
    except ValueError:
        return 0


def to_bool(x: str) -> bool:
    if not isinstance(x, str):
        return False
    if x == "30 min - Paid":
        return True
    return False


@cleaner
def clean_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Forces all columns to the correct type.
    """
    # NAME (string)
    df["Name"] = df["Name"].apply(to_str).astype("string")
    # PAYROLL ID (int)
    df["Payroll ID"] = df["Payroll ID"].apply(to_int).astype("int64")
    # CLOCK IN DATETIME (datetime)
    df["Clock in datetime"] = df["Clock in date"] + df["Clock in time"]
    df["Clock in datetime"] = (
        df["Clock in datetime"]
        .apply(to_str)
        .apply(to_datetime)
        .astype("datetime64[ns]")
    )
    # CLOCK OUT DATETIME (datetime)
    df["Clock out datetime"] = df["Clock out date"] + df["Clock out time"]
    df["Clock out datetime"] = (
        df["Clock out datetime"]
        .apply(to_str)
        .apply(to_datetime)
        .astype("datetime64[ns]")
    )
    # BREAK START (datetime)
    df["Break start"] = df["Clock in date"] + df["Break start"]
    df["Break start"] = (
        df["Break start"].apply(to_str).apply(to_datetime).astype("datetime64[ns]")
    )
    # BREAK END (datetime)
    df["Break end"] = df["Clock in date"] + df["Break end"]
    df["Break end"] = (
        df["Break end"].apply(to_str).apply(to_datetime).astype("datetime64[ns]")
    )
    # ROLE (string)
    df["Role"] = df["Role"].apply(to_str, placeholder="None").astype("string")
    # WAGE (int)
    df["Wage"] = df["Wage"].apply(to_currency).astype("int64")
    # SCHEDULED HOURS (int)
    df["Scheduled"] = df["Scheduled"].apply(to_currency).astype("int64")
    # ISSUES (string)
    df["Issues"] = df["Issues"].apply(to_str, placeholder="").astype("string")
    # EMPLOYEE NOTE (string)
    df["Employee Note"] = (
        df["Employee Note"].apply(to_str, placeholder="").astype("string")
    )
    # MANAGER NOTE (string)
    df["Manager Note"] = (
        df["Manager Note"].apply(to_str, placeholder="").astype("string")
    )
    # BREAK PAID (bool)
    df["Break paid"] = df["Break type"].apply(to_bool).astype("bool")

    return df
