def make_filename(data_dir="data"):
    from datetime import date
    # month = date.today().strftime('%b_%Y')
    year_month = date.today().strftime('%Y-%b')
    return f"{data_dir}/{year_month}_temperatures.csv"


# for some reason, function names don't like dashes. So, a literal `dash` gets 
# spelt out. For some reason...
def make_filename_YEAR_dash_MON_directory():
    from datetime import date
    year_month = date.today().strftime('%Y-%b')
    return f"{year_month}"


def make_filename_with_ISO_date(data_dir="data"):
    from datetime import date
    year_month_date = date.today().strftime('%Y-%m-%d')
    return f"{data_dir}/{year_month_date}_temperatures.csv"
