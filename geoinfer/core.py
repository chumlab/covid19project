import re
import pandas as pd
import numpy as np

from .constants import LOCATION_DISCARD, AS_IS_LOCATIONS

"""
### Core infering functions
"""

def get_country(countries_df, element):
    # Filter 'Country' field with 'element'
    country = countries_df[countries_df['Country'] == element]
    
    # No results
    if len(country) == 0:
        return None
    
    # There can be only one result
    return country


def get_admin1(admin1_df, element, country_code=None):
    if country_code is None:
        # admin1 matching name (or ascii name), or admin1 code w/o country
        admin1 = admin1_df[(admin1_df['name'] == element) | \
                           (admin1_df['name ascii'] == element) | \
                           (admin1_df['code'].str.contains(rf'.{element}$'))]
        
        if len(admin1) == 0:
            # No results
            return None
    
        if len(admin1) > 1:
            # If it's an admin1 code
            if len(element) == 2:
                # If there's more than 1 admin1 codes and it's a 2 letter code,
                # take the one that is either USA or Canada
                admin1_ = admin1.copy()
                admin1 = admin1_[(admin1_['code'].str.contains(rf'us.{element}$')) | \
                                 (admin1_['code'].str.contains(rf'ca.{element}$'))]
                
                if len(admin1) == 1:
                    return admin1
                
                else:
                    # #ERROR:99
                    # This error happens when for an admin1 code,
                    # w/o a country, there is more than 1 admin1 row that is not USA or Canada
                    admin1 = admin1_df[admin1_df['code'].str.contains(rf'.{element}$')].copy()
                    admin1.loc[:, 'geonameid'] = 99
                    return admin1.head(1)
            
            # If there's more than 1 admin1 name/ascii name
            # take the one that is either USA or Canada
            # (Americans tend to write only their state
            # name and e.g. there's many Floridas)
            admin1_ = admin1.copy()
            admin1 = admin1_[(admin1_['code'].str.contains(rf'^us.')) | \
                            (admin1_['code'].str.contains(rf'^ca.'))]
            
            if len(admin1) == 1:
                return admin1
                
            else:
                # #ERROR:98
                # This error happens when, w/o a country, there is
                # more than 1 admin1 by that name/ascii name.
                # There is not enough data to infer which one.
                # (and it's not in the US or Canada)
                # e.g. "La Paz" district (Bolivia, Honduras, El Savador)
                admin1 = admin1_df[(admin1_df['name'] == element)].copy()
                admin1.loc[:, 'geonameid'] = 98
                return admin1.head(1)
    
    else:
        country_code = country_code.lower()
        # admin1 code matching <country_code>.<abbreviation>
        # or (admin1 code starts with <country_code> and (match name (or ascii name)))
        admin1 = admin1_df[
            (admin1_df['code'] == f'{country_code}.{element}') | \
                ((admin1_df['code'].str.contains(rf'^{country_code}.')) & \
                 ((admin1_df['name'] == element) | (admin1_df['name ascii'] == element)))]
        
        if len(admin1) == 0:
            # No results
            return None
        
        if len(admin1) > 1:
            # #ERROR:97
            # This error happens when, with a country, there is
            # more than 1 admin1 by that name/ascii name.
            admin1 = admin1_df[(admin1_df['name'] == element)].copy()
            admin1.loc[:, 'geonameid'] = 97
            return admin1.head(1)
    
    return admin1


def get_city(cities_df, element, admin1_code=None, country_code=None):
    # print(f'admin1_code: {admin1_code}, country_code: {country_code}')
    if admin1_code is None and country_code is None:
        cities = cities_df[(cities_df['altname'] == element)]
    
    elif admin1_code is None:
        cities = cities_df[(cities_df['altname'] == element) & \
                         (cities_df['country'] == country_code)]
    
    elif country_code is None:
        cities = cities_df[(cities_df['altname'] == element) & \
                           (cities_df['admin1'] == admin1_code)]
    
    else:
        cities = cities_df[(cities_df['altname'] == element) & \
                           (cities_df['admin1'] == admin1_code) & \
                           (cities_df['country'] == country_code)]
    
    if len(cities) == 0:
        # No results
        return None
    
    else:
        # More than one result,
        # take the city with the largest population.
        cities = cities.copy()
        cities['population'] = cities['population'].astype('int')
        return cities.nlargest(1, ['population']) 


"""
Cases:

country

city, state/prov, country
city, state/prov
city, country
city

neighboorhood, city, country
neighboorhood, city

state/prov, country
state/prov
"""


# Filter out Regex 'metacharacters' (compile regex for performance)
# https://docs.python.org/3/howto/regex.html#matching-characters
meta_chars = ".^$*+?{}[]\|()"
meta_chars = [re.escape(i) for i in list(meta_chars)]
regrex_pattern = re.compile("|".join(meta_chars))


def infer_geonameid_from_elements(elements, cities_df, admin1_df, countries_df):
    try:
        return compute_geonameid_from_elements(elements, cities_df, admin1_df, countries_df)
    except ValueError:
        return np.nan


def compute_geonameid_from_elements(elements, cities_df, admin1_df, countries_df):
    # Datasets
    # * countries_df
    # * admin1_df
    # * cities_df

    # Remove leading/trailing spaces, lowercase
    elements = [e.strip().lower() for e in elements]
    
    # Don't try to infer if element should be ignored
    if elements[0] in LOCATION_DISCARD:
        return np.nan
    
    # Filter out Regex 'metacharacters'
    elements = [regrex_pattern.sub(r'', e) for e in elements]
    
    # One item
    # TODO: Invert? Check city first, then state, then country?
    # e.g. New York is always the city, not the state.
    if len(elements) == 1:
        country = get_country(countries_df, elements[0])
        
        # "<country>" as-is
        if country is not None:
            return str(country['geonameid'].item())
    
        admin1 = get_admin1(admin1_df, elements[0])
    
        # "<state/province>" as-is
        if admin1 is not None:
            return str(admin1['geonameid'].item())

        city = get_city(cities_df, elements[0])
        
        # "<city>" as-is
        if city is not None:
            return str(city['geonameid'].item())

    
    # Two items (0, 1)
    elif len(elements) == 2:
        country = get_country(countries_df, elements[1])
        
        # if element[1] is country:
        if country is not None:
            country_code = str(country['#ISO'].item())
            
            # Get admin1 (restrict to <country>)
            admin1 = get_admin1(admin1_df, elements[0], country_code=country_code)
    
            # if element[0] is <state/province> within <country>:
            if admin1 is not None:
                return str(admin1['geonameid'].item())
            
            # Get city (restrict to <country>)
            city = get_city(cities_df, elements[0], country_code=country_code)
        
            # if element[0] is <city> within <country>:
            if city is not None:
                return str(city['geonameid'].item())
                
            # return country
            return str(country['geonameid'].item())
        
        
        admin1 = get_admin1(admin1_df, elements[1])
        
        # if element[1] is <state/province>:
        if admin1 is not None:
            
            # Format is '<COUNTRY_CODE>.<ADMIN1_CODE>'
            # Split it, then make it into a tuple
            country_code, admin1_code = tuple(str(admin1['code'].item()).split('.'))
            
            # Get city (restrict to <state/province>)
            city = get_city(cities_df, elements[0], admin1_code=admin1_code)
            
            # if element[0] is <city> within <country>:
            if city is not None:
                return str(city['geonameid'].item())
                
            # return <state/province>
            return str(admin1['geonameid'].item())
         
        city = get_city(cities_df, elements[1])
        
        # if element[1] is <city>:
        if city is not None:
            return str(city['geonameid'].item())
    
    # Three items
    elif len(elements) == 3:
        
        country = get_country(countries_df, elements[2])
        
        # if element[2] is country:
        if country is not None:
            country_code = str(country['#ISO'].item())

            # Get admin1 (restrict to <country>)
            admin1 = get_admin1(admin1_df, elements[1], country_code=country_code)
            
            # if element[1] is <state/province> within <country>:
            if admin1 is not None:
                
                # Format is '<COUNTRY_CODE>.<ADMIN1_CODE>'
                # Split it, then make it into a tuple
                country_code, admin1_code = tuple(str(admin1['code'].item()).split('.'))
                
                # Get city (restrict to <state/province>)
                city = get_city(cities_df, elements[0], admin1_code=admin1_code)
                
                # if element[0] if <city> within <state/province>
                if city is not None:
                    # return <city>
                    return str(city['geonameid'].item())
                   
                # return <state/province>
                return str(admin1['geonameid'].item())
                
            # Get city (restrict to <state/province>)
            city = get_city(cities_df, elements[1], country_code=country_code)
                
            # if element[1] is <city> within <country>:
            if city is not None:
                # return <city>
                return str(city['geonameid'].item())
                
            # return country
            return str(country['geonameid'].item())
            
        admin1 = get_admin1(admin1_df, elements[2])
        
        # if element[2] is <state/province>:
        if admin1 is not None:
            
            # Format is '<COUNTRY_CODE>.<ADMIN1_CODE>'
            # Split it, then make it into a tuple
            country_code, admin1_code = tuple(str(admin1['code'].item()).split('.'))
            
            # Get city (restrict to <state/province>)
            city = get_city(cities_df, elements[1], admin1_code=admin1_code)
            
            # if element[1] if <city> within <state/province>
            if city is not None:
                # return <city>
                return str(city['geonameid'].item())
            
    return np.nan

"""
### Inferrance entrypoint
"""
def infer_geonameid(df, cities_df, admin1_df, countries_df):
    # Infer
    df['geonameid'] = df['elements'].map(lambda elements:
        infer_geonameid_from_elements(elements, cities_df, admin1_df, countries_df))

    # Substitute "as-is" locations
    for location, geonameid in AS_IS_LOCATIONS.items():
        df.loc[(df['tweet_user_location'] == location),'geonameid'] = geonameid

    return df