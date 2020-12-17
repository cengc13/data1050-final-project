import logging
import pymongo
import pandas as pd
import expiringdict
import time
import utils

client = pymongo.MongoClient()
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'db.log')
RESULT_CACHE_EXPIRATION = 3600 * 24          # seconds

levels = ['covid-us', 'covid-us-state', 'mask-use-by-county', 'state-population',
         'county-population', 'fips_code', 'state-area']

def fetch_all_db():
    db = client.get_database("covid-us")
    ret_dict = {}
    for level in levels:
        collection = db.get_collection(level)
        ret = list(collection.find())
        ret_dict[level] = ret
        logger.info(str(len(ret)) + ' documents read from the db')
        time.sleep(60)
    return ret_dict


_fetch_all_db_as_df_cache = expiringdict.ExpiringDict(max_len=10,
                                                       max_age_seconds=RESULT_CACHE_EXPIRATION)


def fetch_all_db_as_df(allow_cached=False):
    """Converts list of dicts returned by `fetch_all_db` to DataFrame with ID removed
    Actual job is done in `_worker`. When `allow_cached`, attempt to retrieve timed cached from
    `_fetch_all_db_as_df_cache`; ignore cache and call `_work` if cache expires or `allow_cached`
    is False.
    """
    def _work():
        ret_dict = fetch_all_db()
        if len(ret_dict) != 7:
            return _work()
        df_dict = {}
        for level, data in ret_dict.items():
            df = pd.DataFrame.from_records(data)
            df.drop('_id', axis=1, inplace=True)
            df.columns = map(str.lower, df.columns)
            df_dict[level] = df
        return df_dict

    if allow_cached:
        try:
            return _fetch_all_db_as_df_cache['cache']
        except KeyError:
            pass
    ret = _work()
    _fetch_all_db_as_df_cache['cache'] = ret
    return ret


if __name__ == '__main__':
    print(fetch_all_db_as_df())
