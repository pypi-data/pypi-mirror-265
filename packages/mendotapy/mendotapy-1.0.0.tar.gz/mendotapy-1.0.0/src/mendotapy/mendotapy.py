import calendar
from datetime import datetime
import requests

from bs4 import BeautifulSoup
import pandas as pd


def _month_to_number(month):
    """convert string to month number otherwise 0"""
    if isinstance(month, str):
        month_dict = {mon.lower(): idx for idx, mon in enumerate(calendar.month_name)}
        return month_dict.get(month.lower(), 0)
    else:
        return 0


def _extract_year(row, month_column):
    """extracts year winter column"""
    splits = row["Winter"].split("-")
    season_start = splits[0]
    season_end = splits[1]

    candidate_century = season_start[0:2]

    if season_end == "00":
        century = int(candidate_century) + 1
    else:
        century = candidate_century

    winter_with_century = f"{season_start}-{century}{season_end}"

    year_range = winter_with_century.split("-")

    if row[month_column] < 7:
        return year_range[1]
    else:
        return year_range[0]


def __get_raw_data(url: str = None):
    """reads raw data from URL"""
    if url is None:
        url = (
            "https://climatology.nelson.wisc.edu"
            "/first-order-station-climate-data/madison-climate"
            "/lake-ice/history-of-ice-freezing-and-thawing-on-lake-mendota/"
        )

    data = requests.get(url)
    html_content = data.text

    soup = BeautifulSoup(html_content, "html.parser")
    table_id = "ice-table"

    try:
        table = soup.find("table", {"id": table_id})
        rows = table.find_all("tr")

        data = []

        for row in rows:
            row_headers = row.find_all("th")
            if row_headers:
                headers = [col.text.strip() for col in row_headers]
            cols = row.find_all("td")
            cols = [col.text.strip() for col in cols]

            if cols:
                data.append(cols)

        df = pd.DataFrame(data, columns=headers).replace("–", pd.NA)
        return df

    except AttributeError as e:
        print(f"{e}")
        print(f"Check that {table_id} is the correct table id")


def __process_data(df):
    """process data, this could be refactored"""

    # convert Gregorian dates to numeric values
    df[["iceon_month", "iceon_day"]] = df["Freeze-Over Date"].str.split(expand=True)
    df["iceon_month"] = df["iceon_month"].apply(_month_to_number)
    df["iceon_day"] = pd.to_numeric(df["iceon_day"])
    df["iceon_month"] = pd.to_numeric(df["iceon_month"])

    df[["iceoff_month", "iceoff_day"]] = df["Thaw Date"].str.split(expand=True)
    df["iceoff_month"] = df["iceoff_month"].apply(_month_to_number)
    df["iceoff_day"] = pd.to_numeric(df["iceoff_day"])
    df["iceoff_month"] = pd.to_numeric(df["iceoff_month"])

    # extract iceon and iceoff year
    df["iceon_year"] = df.apply(lambda row: _extract_year(row, "iceon_month"), axis=1)
    df["iceoff_year"] = df.apply(lambda row: _extract_year(row, "iceoff_month"), axis=1)

    # additional columns consistent with NSIDC Global Lake and River Ice Phenology database
    df["latitude"] = 43.100
    df["longitude"] = -89.400
    df["lakename"] = "LAKE MENDOTA"
    df["lakecode"] = "DMR1"
    df["froze"] = "Y"
    df["lakeriver"] = "L"
    df["country"] = "UNITED STATES"

    # rename to be consistent with NSIDC database
    df = df.rename(columns={"Winter": "season", "Days of Ice Cover": "duration"})

    df["duration"] = df["duration"].replace("", "-999")

    df = df.fillna(-999).astype(
        {
            "season": str,
            "iceon_year": int,
            "iceon_month": int,
            "iceon_day": int,
            "iceoff_year": int,
            "iceoff_month": int,
            "iceoff_day": int,
            "duration": int,
            "latitude": float,
            "longitude": float,
            "lakename": str,
            "lakecode": str,
            "froze": str,
            "lakeriver": str,
            "country": str,
        }
    )

    # replace -999 values in duration with None
    # this needs to be done after changing the type
    df["duration"] = df["duration"].replace(-999, None)

    columns = [
        "season",
        "iceon_year",
        "iceon_month",
        "iceon_day",
        "iceoff_year",
        "iceoff_month",
        "iceoff_day",
        "duration",
        "latitude",
        "longitude",
        "lakename",
        "lakecode",
    ]

    df = df.loc[:, columns]
    return df


def load():
    """load analysis-ready Lake Mendota ice phenology

    Returns
    -------
        pandas.DataFrame: anlysis-ready ice phenology

    Example
    -------
    import mendotapy
    df = mendotapy.load()
    """
    df = __get_raw_data()
    return __process_data(df)


@pd.api.extensions.register_dataframe_accessor("utils")
class MendotapyAccessor:
    def __init__(self, df):
        self._df = df

    def _ymd_to_doy(self, year: int, month: int, day: int):
        """year month day to day of year"""
        return datetime(year, month, day).timetuple().tm_yday

    def iceon_doy(self):
        """ice on day of year

        Returns
        -------
            list: ice on day of year
        """
        doy_list = []
        for index, row in self._df.iterrows():
            year = row["iceon_year"]
            month = row["iceon_month"]
            day = row["iceon_day"]
            try:
                doy = self._ymd_to_doy(year=year, month=month, day=day)
                doy_list.append(doy)
            except ValueError:
                doy_list.append(None)
        return doy_list

    def iceon_doy_wrapped(self):
        """ice on day of year,
        where values greater than 365 indicate the **following** year

        Returns
        -------
            list: ice on day of year
        """
        doy_list = []
        for index, row in self._df.iterrows():
            year = row["iceon_year"]
            month = row["iceon_month"]
            day = row["iceon_day"]
            try:
                doy = self._ymd_to_doy(year=year, month=month, day=day)
                if doy < 182:
                    days_in_previous_year = self._ymd_to_doy(
                        year=year - 1, month=12, day=31
                    )
                    doy = doy + days_in_previous_year
                doy_list.append(doy)
            except ValueError:
                doy_list.append(None)
        return doy_list

    def iceoff_doy(self):
        """ice off day of year,

        Returns
        -------
            list: ice off day of year
        """
        doy_list = []
        for index, row in self._df.iterrows():
            year = row["iceoff_year"]
            month = row["iceoff_month"]
            day = row["iceoff_day"]
            try:
                doy = self._ymd_to_doy(year=year, month=month, day=day)
                doy_list.append(doy)
            except ValueError:
                doy_list.append(None)
        return doy_list

    def iceoff_doy_wrapped(self):
        """ice off day of year,
        where values less than 0 indicate the **previous** year

        Returns
        -------
            list: ice off day of year
        """
        doy_list = []
        for index, row in self._df.iterrows():
            year = row["iceoff_year"]
            month = row["iceoff_month"]
            day = row["iceoff_day"]
            try:
                doy = self._ymd_to_doy(year=year, month=month, day=day)
                if doy > 182:
                    days_in_previous_year = self._ymd_to_doy(
                        year=year, month=12, day=31
                    )
                    doy = doy - days_in_previous_year
                doy_list.append(doy)
            except ValueError:
                doy_list.append(None)
        return doy_list

    def season_start(self):
        """start of the season

        Returns
        -------
            list: start of the season.
                  e.g., the 2023-2024 winter season return 2023
        """
        season_list = []
        for index, row in self._df.iterrows():
            season = int(row["season"].split("-")[0])
            season_list.append(season)
        return season_list
