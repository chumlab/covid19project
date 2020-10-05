from .loaders import load_ingest_df, load_cities_df, load_countries_df, load_admin1_df
from .transformers import add_canadian_province_codes, add_alt_countries, add_alt_admin1, clean, to_lower, substitute_as_is
from .core import geonameid_from_location

import numpy as np


class geoinfer():
    def __init__(self, tweets_path, cities_path, countries_path, admin1_path):
        print("Loading datasets...")

        # load ingest
        self.df = load_ingest_df(tweets_path)

        # load cities, countries, admin1
        self.cities_df = load_cities_df(cities_path)
        self.countries_df = load_countries_df(countries_path)
        self.admin1_df = load_admin1_df(admin1_path)

        print("Done.")
        print("Augmenting and cleaning data...")

        # Add Canadian provinces
        self.admin1_df, self.cities_df = add_canadian_province_codes(
            self.admin1_df, self.cities_df)

        # Add alternatives (countries)
        self.countries_df = add_alt_countries(self.countries_df)

        # Add alternatives (admin1)
        self.admin1_df = add_alt_admin1(self.admin1_df)

        # Clean ingest
        self.df = clean(self.df)

        # Lowercase comparison fields
        (self.df, self.cities_df, self.admin1_df, self.countries_df) = to_lower(
            self.df, self.cities_df, self.admin1_df, self.countries_df)

        print("Done.")

    def infer_location(self, location):
        """
        Args:
            location: a location string
                e.g. "Los Angeles, CA"
        """
        try:
            return geonameid_from_location(location, self.cities_df, self.admin1_df, self.countries_df)
        except ValueError:
            return np.nan

    def run(self):
        """ Run the actual inferrance"
        """
        print("Inferring geoname IDs (this can take a while)...")

        # Add new (inferred) 'geonameid' column.
        # ('tweet_user_location_copy' is the cleaned and augmented copy of 'tweet_user_location')
        self.df['geonameid'] = self.df['tweet_user_location_copy'].map(
            lambda location: self.infer_location(location))

        # Substitute "as-is" locations
        self.df = substitute_as_is(self.df)

        # Drop the temporary, cleaned up and normalized copy 'tweet_user_location'
        self.df = self.df.drop(['tweet_user_location_copy'], axis=1)

        print("Done.")

        return self.df
