from .loaders import load_ingest_df, load_cities_df, load_countries_df, load_admin1_df
from .transformers import add_canadian_province_codes, add_alt_countries, add_alt_admin1, clean, to_lower
from .core import infer_geonameid

def infer(tweets_path, cities_path, countries_path, admin1_path):
    
    print("Loading datasets...")

    # load ingest
    df = load_ingest_df(tweets_path)

    # load cities, countries, admin1
    cities_df = load_cities_df(cities_path)
    countries_df = load_countries_df(countries_path)
    admin1_df = load_admin1_df(admin1_path)

    print("Done.")
    print("Augmenting and cleaning data...")

    # Add Canadian provinces
    admin1_df, cities_df = add_canadian_province_codes(admin1_df, cities_df)

    # Add alternatives (countries)
    countries_df = add_alt_countries(countries_df)

    # Add alternatives (admin1)
    admin1_df = add_alt_admin1(admin1_df)

    # Clean ingest
    df = clean(df)

    # Lowercase comparison fields
    (df, cities_df, admin1_df, countries_df) = to_lower(df, cities_df, admin1_df, countries_df)

    print("Done.")
    print("Inferring geoname IDs (this can take a while)...")

    # Split on comma (,)
    # Add new 'elements' column ('tweet_user_location_copy' split list), used by the inferance
    df['elements'] = df['tweet_user_location_copy'].map(lambda location: location.split(','))

    # Add new (inferred) 'geonameid' column 
    df = infer_geonameid(df, cities_df, admin1_df, countries_df)

    print("Done.")

    return df