from datetime import datetime
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
