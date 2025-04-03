### temperature_serial_downloader

Just a few hacked-up scripts to help dowlnload temperature data from some Raspberry Pi Picos and Wemos D1 minis, perhaps over wifi, perhaps over UART.

#### TODO
- ###### Move CSV files to new home, instead of living in top level folder.
    - python `path.lib` maybe?!? Or is `os.path` still a thing? Time to get the research on!
- ###### Break up CSV files into indivudual days instead of months
    - `Pandas` can do this, but `awk` might be interesting too.
- ###### give `make_chart.py` and variants the ability to chart arbitrary numbers of days
