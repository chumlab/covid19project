import os
import warnings
import pandas as pd

"""
### Loading functions
"""

def load_ingest_df(ingestpath):
    """ Tweets user locations list
    Loading using pandas' read_csv (tab-deleted) to set 'tweet_id' dtype to int
    locations_clean_user_location.tsv"
    """
    return pd.read_csv(ingestpath, sep='\t', dtype={'tweet_id': int})


def load_cities_df(citiespath):
    """ GeoNames (Cities with > 1000 inabitants)
    https://download.geonames.org/export/dump/cities1000.zip
    Loading using geopandas for geometry (usefulness tbd)
    NB: We can ignore 'DtypeWarning' as we don't need column 13
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cities_df = pd.read_csv(citiespath, sep='\t',
                names=['geonameid', 'name', 'asciiname', 'altnames', 'latitude', 'longitude',
                        'featclass', 'featcode', 'country', 'cc2', 'admin1', 'admin2', 'admin3', 'admin4',
                        'population', 'elevation', 'gtopo30', 'timezone', 'moddate'],
                dtype={'admin3': str}) # Does not work for some reason, hence the warning

    # Alternate City names
    # The cities_df dataframe has an 'altnames' column that are CSVs
    # We transform it to a list then explode each into their own row
    # to make searching easier (and reset the index).
    # The new column 'altname' can be used to search.

    cities_alt_df = cities_df.assign(
        altname=cities_df['altnames'].str.split(',')
        ).explode('altname').reset_index(drop=True)

    return cities_alt_df


def load_countries_df(countriespath):
    """ GeoNames (Countries info)
    https://download.geonames.org/export/dump/countryInfo.txt
    Loading using pandas' read_csv (tab-deleted), ignore lines 1-48
    """
    return pd.read_csv(countriespath, sep='\t', header=49)


def load_admin1_df(admin1path):
    """ GeoNames (states and provinces, admin1)
    https://download.geonames.org/export/dump/admin1CodesASCII.txt
    Loading using pandas' read_csv (tab-deleted),
    Column names from https://download.geonames.org/export/dump/readme.txt
    'code' is '<country>.<admin1 for country>'
    """
    return pd.read_csv(admin1path, sep='\t',
                names=['code', 'name', 'name ascii', 'geonameid'])

