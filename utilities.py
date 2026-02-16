"""helper functions to create consistent filenames"""

from datetime import date, datetime


def make_filename(target_date=None, data_dir=None):
    """basic filename maker"""
    # month = date.today().strftime('%b_%Y')
    if target_date is None:
        year_month = date.today().strftime("%Y-%b")
    else:
        if not isinstance(target_date, date):
            raise TypeError("date must be a vaild datetime.date object")
        year_month = target_date.strftime("%Y-%b")
    if data_dir is not None:
        return f"{data_dir}/{year_month}_temperatures.csv"
    return f"{year_month}_temperatures.csv"


def make_date(year=None, month=None, day=None):
    """takes in some things, maybe numbers, amybe strings, and returns a
    datetime.date object suitable for using to do things with"""
    today = date.today()
    if year is None:
        year = today.year
    if not isinstance(year, int):
        year = int(year)
    if year < 1900:
        raise ValueError("Year is out of bounds, must be in the 20th century or later")
    if year > today.year:
        raise ValueError("Year out of bounds, cannot be in the future")

    if month is None:
        month = today.month
    if not isinstance(month, int):
        if not isinstance(month, str):
            raise TypeError(f"Month needs to an int or string instead of {type(month)}")
        if month.isdigit():
            month = int(month)
        else:
            try:
                if len(month) == 3:
                    temp = datetime.strptime(month, "%b")
                else:
                    temp = datetime.strptime(month, "%B")
            except ValueError as e:
                raise ValueError("Bad month supplied") from e
            month = temp.month
    if month < 1 or month > 12:
        raise ValueError("Month is out of bounds, must be between 1 and 12, inclusive")

    if day is None:
        day = 1
    if not isinstance(day, int):
        day = int(day)
    if day < 1 or day > 31:
        raise ValueError("Day is out of bounds")
    try:
        target = date(year, month, day)
    except ValueError as e:
        raise ValueError(f"Bad Value supplied: {e}") from e
    # except Exception as ee:
    #     raise ee
    return target


def test_make_date(yr: list, mn: list, dy: list):
    """testing how the thing does"""
    for year in yr:
        for month in mn:
            for day in dy:
                try:
                    temp = make_date(year, month, day)
                    temp2 = make_filename(temp)
                    print(
                        f"attempt\t{year}, {month}, {day}:\t\t{temp}\t{temp2}"
                    )
                except Exception as e:
                    print(f"FAIL\t{year}, {month}, {day}:\t\texception: {e}")


# for some reason, function names don't like dashes. So, a literal `dash` gets
# spelt out. For some reason...
def make_filename_YEAR_dash_MON_directory(data_dir=None):
    """make a filename with year, then month"""
    year_month = date.today().strftime("%Y-%b")
    if data_dir is not None:
        return f"{data_dir}/{year_month}_temperatures.csv"
    return f"{year_month}_temperatures.csv"


def make_filename_with_full_date(data_dir=None):
    """make filename with year, then month, then day, so
    in the same order as the ISO format"""
    year_month_date = date.today().strftime("%Y-%b-%d")
    if data_dir is not None:
        return f"{data_dir}/{year_month_date}_temperatures.csv"
    return f"{year_month_date}_temperatures.csv"


if __name__ == "__main__":
    yrs = list(range(2020, 2021))
    for y in ["2020", "2021", 1900, 1899, 2026, "2026", "year zero"]:
        yrs.append(y)
    mnths = list(range(5, 13))
    for m in ["January", "january", "Jan", "jan", "jin", "1", "01"]:
        mnths.append(m)
    dys = list(range(15, 35))
    for d in [0, "0", "-1", 0x00, "1", "2", "03", "04", 0b0010, 0xa0,  "0b0010"]:
        dys.append(d)
    print("Testing make_date function:")
    test_make_date(yrs, mnths, dys)
