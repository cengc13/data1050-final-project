"""
Coronavirus (Covid-19) Data in the United States
"""
import time
import sched
import pandas as pd
import logging
import requests
from io import StringIO
import numpy as np
import pymongo

import utils

urls = {
    'covid-us': "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv",
    'covid-us-state': "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv",
#     'covid-us-county': "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv", # too large, skipped!
    'mask-use-by-county': "https://raw.githubusercontent.com/nytimes/covid-19-data/master/mask-use/mask-use-by-county.csv",
    'state-population': "https://raw.githubusercontent.com/cengc13/data1050-final-project/main/data/PopulationState.csv",
    'county-population': "https://raw.githubusercontent.com/cengc13/data1050-final-project/main/data/PopulationCounty.csv",
    'fips_code': "https://raw.githubusercontent.com/cengc13/data1050-final-project/main/data/fips_code.csv",
}

filters = {
    'covid-us': ['date'],
    'covid-us-state': ['date', 'state'],
#     'covid-us-county': ['date', 'county'], 
    'mask-use-by-county': ['COUNTYFP'],
    'state-population': ['state'],
    'county-population': ['county'],
    'fips_code': ['county']
}

all_states = np.array(['Washington', 'Wisconsin', 'Wyoming', 'Illinois', 'California',
       'Arizona', 'Massachusetts', 'Texas', 'Nebraska', 'Utah', 'Oregon',
       'Florida', 'New York', 'Rhode Island', 'Georgia', 'New Hampshire',
       'North Carolina', 'New Jersey', 'Colorado', 'Maryland', 'Nevada',
       'Tennessee', 'Hawaii', 'Indiana', 'Kentucky', 'Minnesota',
       'Oklahoma', 'Pennsylvania', 'South Carolina',
       'District of Columbia', 'Kansas', 'Missouri', 'Vermont',
       'Virginia', 'Connecticut', 'Iowa', 'Louisiana', 'Ohio', 'Michigan',
       'South Dakota', 'Arkansas', 'Delaware', 'Mississippi',
       'New Mexico', 'North Dakota', 'Alaska', 'Maine', 'Alabama',
       'Idaho', 'Montana', 'Puerto Rico', 'Virgin Islands', 'Guam',
       'West Virginia', 'Northern Mariana Islands'], dtype=object)



# MAX_DOWNLOAD_ATTEMPT = 5
DOWNLOAD_PERIOD = 3600*24        # second, one day update

client = pymongo.MongoClient()
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'data.log')


def download_db(url=urls['covid-us']):
    """Returns US-national Covid-19 data from `NYTIMES_SOURCE` that includes total cases and deaths
    Returns None if network failed
    """
    text = None
    try:
        req = requests.get(url, timeout=0.5)
        req.raise_for_status()
        text = req.text
    except requests.exceptions.HTTPError as e:
        logger.warning("Retry on HTTP Error: {}".format(e))
        return None
    if text is None:
        logger.error('download covid19-us too many FAILED attempts')
    return text


def filter_db(text):
    """Converts `text` to `DataFrame`, removes empty lines and descriptions
    """
    # use StringIO to convert string to a readable buffer
    df = pd.read_csv(StringIO(text), delimiter=',')
    df.columns = df.columns.str.strip()             # remove space in columns name
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    df.dropna(inplace=True)             # drop rows with empty cells
    return df


def upsert_db(df, level='covid-us'):
    """
    Update MongoDB database 'covid-us' and collections with the given `DataFrame`.
    """
    db = client.get_database("covid-us")
    collection = db.get_collection(level)
    update_count = 0
    if level == 'covid-us-county':
        for state in all_states:
            df_state = df[df['state'] == state]
        for record in df_state.to_dict('records'):
            filter_ = {_:record[_] for _ in filters[level]}
            result = collection.replace_one(
                filter=filter_,                             # locate the document if exists
                replacement=record,                         # latest document
                upsert=True)                                # update if exists, insert if not
            if result.matched_count > 0:
                update_count += 1
    else:
        for record in df.to_dict('records'):
            filter_ = {_:record[_] for _ in filters[level]}
            result = collection.replace_one(
                filter=filter_,                             # locate the document if exists
                replacement=record,                         # latest document
                upsert=True)                                # update if exists, insert if not
            if result.matched_count > 0:
                update_count += 1
    logger.info(f"{level.split('-')[-1]}:"
          f"rows={df.shape[0]}, update={update_count}, "
          f"insert={df.shape[0]-update_count}")


def update_once():
    for level, url in urls.items():
        t = download_db(url)
        df = filter_db(t)
        upsert_db(df, level)


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


