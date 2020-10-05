import pandas as pd
import re

from .constants import CAN_PROVINCES_ABREV, ALT_COUNTRY_NAMES, ALT_ADMIN1_NAMES, AS_IS_LOCATIONS

"""
### Augmenting functions
"""


def add_canadian_province_codes(admin1_df, cities_df):
    """ GeoNames 'admin1' (admin1_df) for Canadian provinces uses a 2-digit code
    Use postal abbreviation which people use
    """
    admin1_alt_df = admin1_df.copy()
    for num, alpha in CAN_PROVINCES_ABREV.items():
        admin1_alt_df.loc[(admin1_alt_df['code'] == num), 'code'] = alpha

    # Add to cities too
    # Query the cities with country CA and num code, copy,
    # replace num code by letter code, then concat back
    cities_alt_df = cities_df.copy()
    new_cities = pd.DataFrame([], columns=cities_df.columns)
    for num_code, letter_code in CAN_PROVINCES_ABREV.items():
        country, num = tuple(num_code.split('.'))
        country, letter = tuple(letter_code.split('.'))

        alt_cities = cities_df[(cities_df['country'] == country) &
                               (cities_df['admin1'] == num)].copy()
        alt_cities['admin1'] = letter
        new_cities = pd.concat([new_cities, alt_cities], ignore_index=True)

    cities_alt_df = pd.concat([cities_alt_df, new_cities], ignore_index=True)

    # Return like original arguments
    return (admin1_alt_df, cities_alt_df)


def add_alt_countries(countries_df):
    """ Add alternative country names (e.g. USA, UK, etc.)
    Copy the row of the country and replace its name with the alternative
    """
    new_countries = pd.DataFrame([], columns=countries_df.columns)
    for geo, alt_names in ALT_COUNTRY_NAMES.items():
        for name in alt_names:
            alt_country = countries_df[countries_df['geonameid'] == geo].copy()
            alt_country['Country'] = name
            new_countries = pd.concat(
                [new_countries, alt_country], ignore_index=True)

    return pd.concat([countries_df, new_countries], ignore_index=True)


def add_alt_admin1(admin1_df):
    """ Add alternative admin1 names
    Copy the row of the admin1 and replace its name with the alternative
    """
    new_admin1s = pd.DataFrame([], columns=admin1_df.columns)
    for geo, alt_names in ALT_ADMIN1_NAMES.items():
        for name in alt_names:
            alt_admin1 = admin1_df[admin1_df['geonameid'] == geo].copy()
            alt_admin1['name'] = name
            alt_admin1['name ascii'] = name
            new_admin1s = pd.concat(
                [new_admin1s, alt_admin1], ignore_index=True)

    return pd.concat([admin1_df, new_admin1s], ignore_index=True)


def clean(df):
    """ General 'tweet_user_location' cleaning rules
    Adds a new 'tweet_user_location_copy' column to leave the original intact
    """
    # Make a copy of 'tweet_user_location' so we leave the original intact
    df['tweet_user_location_copy'] = df['tweet_user_location']

    # Discard locations that don't exist more than 2 times
    df = df[df['tweet_id'] > 2]

    # Filter out emojis and other symbols
    # * https://stackoverflow.com/a/49986645
    # * https://www.ling.upenn.edu/courses/Spring_2003/ling538/UnicodeRanges.html (Unicode symbol ranges)
    def deEmojify(text):
        regrex_pattern = re.compile(pattern="["
                                    u"\U0001F600-\U0001F64F"  # emojis: emoticons
                                    u"\U0001F300-\U0001F5FF"  # emojis: symbols & pictographs
                                    u"\U0001F680-\U0001F6FF"  # emojis: transport & map symbols
                                    u"\U00002700-\U000027BF"  # 'Dingbats' http://www.unicode.org/charts/PDF/U2700.pdf
                                    "]+", flags=re.UNICODE)
        return regrex_pattern.sub(r'', text)
    df['tweet_user_location_copy'] = df['tweet_user_location_copy'].map(
        lambda x: deEmojify(x))

    # Truncate leading and trailing spaces
    df['tweet_user_location_copy'] = df['tweet_user_location_copy'].map(
        lambda x: x.strip())

    # Filter out emoji flags, except if there's only one
    # n.b. 1 emoji = 2 characters (i.e. '{2}')
    def deFlag(text):
        regrex_oneflag = re.compile(
            pattern=u"^[\U0001F1E0-\U0001F1FF]{2}$", flags=re.UNICODE)
        regrex_allflags = re.compile(
            pattern=u"[\U0001F1E0-\U0001F1FF]+", flags=re.UNICODE)
        if regrex_oneflag.search(text) is not None:
            return text
        else:
            return regrex_allflags.sub(r'', text)

    df['tweet_user_location_copy'] = df['tweet_user_location_copy'].map(
        lambda x: deFlag(x))

    # Truncate trailing "," and "." characters
    df['tweet_user_location_copy'] = df['tweet_user_location_copy'].map(
        lambda x: x.rstrip(','))
    df['tweet_user_location_copy'] = df['tweet_user_location_copy'].map(
        lambda x: x.rstrip('.'))

    return df


def to_lower(df, cities_df, admin1_df, countries_df):
    """ Make some fields lowercase to help with comparisons
    """
    # Locations
    df['tweet_user_location_copy'] = df['tweet_user_location_copy'].str.lower()

    # Cities
    cities_df['name'] = cities_df['name'].str.lower()
    cities_df['asciiname'] = cities_df['asciiname'].str.lower()
    cities_df['altname'] = cities_df['altname'].str.lower()
    cities_df['admin1'] = cities_df['admin1'].str.lower()

    # Admin1
    admin1_df['code'] = admin1_df['code'].str.lower()
    admin1_df['name'] = admin1_df['name'].str.lower()
    admin1_df['name ascii'] = admin1_df['name ascii'].str.lower()

    # Countries
    countries_df['Country'] = countries_df['Country'].str.lower()

    return (df, cities_df, admin1_df, countries_df)


def substitute_as_is(df):
    for location, geonameid in AS_IS_LOCATIONS.items():
        df.loc[(df['tweet_user_location'] == location),
               'geonameid'] = geonameid

    return df
