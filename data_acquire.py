"""
Bonneville Power Administration, United States Department of Energy
"""
import time
import sched
import pandas
import logging
import requests
from io import StringIO

import utils
from database import upsert_db


# BPA_SOURCE = "https://transmission.bpa.gov/business/operations/Wind/baltwg.txt"
BPA_SOURCE = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"
MAX_DOWNLOAD_ATTEMPT = 5
DOWNLOAD_PERIOD = 60        # second
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'data.log')


def download_db(url=BPA_SOURCE, retries=MAX_DOWNLOAD_ATTEMPT):
    """Returns US-national Covid-19 data from `NYTIMES_SOURCE` that includes total cases and deaths
    Returns None if network failed
    """
    text = None
    for i in range(retries):
        try:
            req = requests.get(url, timeout=0.5)
            req.raise_for_status()
            text = req.text
        except requests.exceptions.HTTPError as e:
            logger.warning("Retry on HTTP Error: {}".format(e))
    if text is None:
        logger.error('download_covid19-us too many FAILED attempts')
    return text


def filter_db(text):
    """Converts `text` to `DataFrame`, removes empty lines and descriptions
    """
    # use StringIO to convert string to a readable buffer
    df = pandas.read_csv(StringIO(text), delimiter=',')
    df.columns = df.columns.str.strip()             # remove space in columns name
    df['Date'] = pandas.to_datetime(df['Date'])
    df.dropna(inplace=True)             # drop rows with empty cells
    return df


def update_once():
    t = download_db()
    df = filter_db(t)
    upsert_db(df)


def main_loop(timeout=DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
        try:
            update_once()
        except Exception as e:
            logger.warning("main loop worker ignores exception and continues: {}".format(e))
        scheduler.enter(timeout, 1, _worker)    # schedule the next event

    scheduler.enter(0, 1, _worker)              # start the first event
    scheduler.run(blocking=True)


if __name__ == '__main__':
    main_loop()


