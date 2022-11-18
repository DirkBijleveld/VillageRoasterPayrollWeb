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


@cleaner
def clean_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Forces all columns to be the correct type.
    This is the most fundamentally complex and important part of the cleaning process.
    This has been the source of 99% of bugs with the software...
    """
    # NAME
    # Fill empty (NaN) values with empty strings (otherwise forcing type causes an error)
    df["Name"] = df["Name"].fillna("")
    # Force type to string
    df["Name"] = df["Name"].astype(str)
    # Remove leading and trailing whitespace
    df["Name"] = df["Name"].str.strip()

    # PAYROLL ID
    # Fill empty (NaN) values with 9999 (otherwise forcing type causes an error)
    df["Payroll ID"] = df["Payroll ID"].fillna(9999)
    # Force type to integer

    def payroll_id_to_int(payroll_id) -> int:
        """
        Converts a payroll ID to an integer.
        Local function because it's only used in this one place.
        try: except: is usually bad practice, but this piece is integral to functionality.
        Finally, any problems with the Payroll ID can and will be resolved manually later,
        so the cost of missing one minor rare exception is worth the cost of not crashing.
        """
        try:
            return int(payroll_id)
        except ValueError:
            return 9999

    df["Payroll ID"] = df["Payroll ID"].apply(payroll_id_to_int)

    # CLOCK IN DATETIME

    def as_datetime(s: str, can_null: bool = True) -> datetime | None:
        """
        Converts a date and time to a datetime object.
        Local function because it's only used in this one place.
        """
        try:
            return datetime.strptime(f"{s}", "%d %B %Y%I:%M%p")
        except ValueError:
            if can_null:
                return None
            raise ValueError(f"Failed to construct datetime out of input {s}")

    df["Clock in datetime"] = df["Clock in date"] + df["Clock in time"]
    df["Clock in datetime"] = df["Clock in datetime"].apply(as_datetime)

    # CLOCK OUT DATETIME
    df["Clock out datetime"] = df["Clock out date"] + df["Clock out time"]
    df["Clock out datetime"] = df["Clock out datetime"].apply(as_datetime)

    # BREAK START
    df["Break start"] = df["Clock in date"] + df["Break start"]
    df["Break start"] = df["Break start"].apply(as_datetime)

    # BREAK END
    df["Break end"] = df["Clock in date"] + df["Break end"]
    df["Break end"] = df["Break end"].apply(as_datetime)

    # ROLE
    df["Role"] = df["Role"].fillna("None")
    df["Role"] = df["Role"].astype(str)

    # WAGE
    df["Wage"] = df["Wage"].fillna("0")

    def wage_fix(wage) -> str:
        try:
            return str(wage)
        except ValueError:
            return "0"

    df["Wage"] = df["Wage"].apply(wage_fix)
    df["Wage"] = df["Wage"].apply(lambda wage: Decimal(wage.strip("$").strip(",")))

    def wage_int(wage: Decimal) -> int:
        return int(wage * 1000)

    df["Wage"] = df["Wage"].apply(wage_int)

    # SCHEDULED HOURS
    df["Scheduled"] = df["Scheduled"].fillna("0")

    def scheduled_fix(scheduled) -> str:
        try:
            return str(scheduled)
        except ValueError:
            return "0"

    df["Scheduled"] = df["Scheduled"].apply(scheduled_fix)
    df["Scheduled"] = df["Scheduled"].apply(lambda scheduled: Decimal(scheduled.strip("$").strip(",")))

    def scheduled_int(scheduled: Decimal) -> int:
        return int(scheduled * 1000)

    df["Scheduled"] = df["Scheduled"].apply(scheduled_int)

    # ISSUES COLUMN
    if "Issues" not in df:
        df["Issues"] = ""
    df["Issues"] = df["Issues"].fillna("")

    def issues_fix(issues) -> str:
        try:
            return str(issues)
        except ValueError:
            return ""

    df["Issues"] = df["Issues"].apply(issues_fix)

    # EMPLOYEE NOTE COLUMN
    if "Employee note" not in df:
        df["Employee note"] = ""
    df["Employee note"] = df["Employee note"].fillna("")

    def employee_note_fix(employee_note) -> str:
        try:
            return str(employee_note)
        except ValueError:
            return ""

    df["Employee note"] = df["Employee note"].apply(employee_note_fix)

    # MANAGER NOTE COLUMN
    if "Manager note" not in df:
        df["Manager note"] = ""

    df["Manager note"] = df["Manager note"].fillna("")

    def manager_note_fix(manager_note) -> str:
        try:
            return str(manager_note)
        except ValueError:
            return ""

    df["Manager note"] = df["Manager note"].apply(manager_note_fix)

    # BREAK PAID BOOLEAN
    def break_paid_fix(break_paid) -> bool:
        if not isinstance(break_paid, str):
            return False
        if break_paid == "30 min - Paid":
            return True
        return False

    df["Break paid"] = df["Break type"].apply(break_paid_fix)

    return df
