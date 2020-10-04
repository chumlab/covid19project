import pandas as pd

from .constants import LOCATION_DISCARD

"""
### Utils functions
"""

def print_geonameid_completeness(df):
    """ Displays the percentage of tweets that have a 'geonameid'
    Skipping the ones we know aren't valid (discards)
    """
    all_tweets = df[~df['tweet_user_location_copy'].isin(LOCATION_DISCARD)]['tweet_id'].sum()
    geonameid_tweets = df[df.geonameid.notnull()]['tweet_id'].sum()
    print(f'{geonameid_tweets/all_tweets*100:.3f}%')


def show_nan(df):
    """ Show dataframe df where 'geonameid' is NaN and location
    is not known to be invalid (discards)
    """
    nan_df = df[(~df['tweet_user_location_copy'].isin(LOCATION_DISCARD)) & df['geonameid'].isnull()]
    print(f'Number of NaNs: {len(nan_df.index)}')
    return nan_df