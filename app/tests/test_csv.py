from pathlib import Path

import pandas as pd
from pytest import fixture


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
def df_fake() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Name": ["John", "Jane", "Joe"],
            "Clock in date": ["2021-01-01", "2021-01-01", "2021-01-01"],
            "Clock in time": ["8:00am", "8:00am", "8:00am"],
            "Clock out date": ["2021-01-01", "2021-01-01", "2021-01-01"],
            "Clock out time": ["4:00pm", "4:00pm", "4:00pm"],
            "Break start": ["", "", ""],
            "Break end": ["", "", ""],
            "Break length": ["", "", ""],
            "Break type": ["", "", ""],
            "Payroll ID": [1, 2, 3],
            "Role": ["Admin", "Main Store", "Hospital"],
            "Wage": ["$16.00", "$16.00", "$16.00"],
            "Scheduled": ["", "", ""],
            "Actual vs. Scheduled": ["", "", ""],
            "Total Paid": ["8.0", "8.0", "8.0"],
            "Regular": ["", "", ""],
            "Unpaid Breaks": ["", "", ""],
            "Overtime": ["", "", ""],
            "Est. Wages": ["", "", ""],
            "Cash Tips": ["", "", ""],
            "Issues": ["", "", ""],
            "No Show Reason": ["", "", ""],
            "Employee Note": ["", "", ""],
            "Manager Note": ["", "", ""],
        }
    )
