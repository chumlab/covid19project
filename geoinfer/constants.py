""" GeoNames 'admin1' (admin1_df) for Canadian provinces uses a 2-digit code
Use postal abbreviation which people use
"""

CAN_PROVINCES_ABREV = {
    'CA.01': 'CA.AB', # Alberta
    'CA.02': 'CA.BC', # British Columbia
    'CA.03': 'CA.MB', # Manitoba
    'CA.04': 'CA.NB', # New Brunswick
    'CA.05': 'CA.NL', # Newfoundland and Labrador
    'CA.07': 'CA.NS', # Nova Scotia
    'CA.08': 'CA.ON', # Ontario
    'CA.09': 'CA.PE', # Prince Edward Island
    'CA.10': 'CA.QC', # Quebec
    'CA.11': 'CA.SK', # Saskatchewan
    'CA.12': 'CA.YK', # Yukon
    'CA.13': 'CA.NT', # Northwest Territories
    'CA.14': 'CA.NU'  # Nunavut
}


""" Alternative country names (e.g. USA, UK, etc.)
(we can't easily get alternative country names)
"""

ALT_COUNTRY_NAMES = {
    6252001: ['USA', 'US','United States of America','America', 'Estados Unidos', '🇺🇸'], # United States
    2510769: ['España', 'Espanya', '🇪🇸'], # [Kingdom of] Spain
    2635167: ['UK', '🇬🇧'], # United Kingdom
    1861060: ['日本', '🇯🇵'],    # Japan
    298795: ['Türkiye', '🇹🇷'], # Turkey
    3469034: ['Brasil', '🇧🇷'], # Brazil
    3175395: ['Italia', '🇮🇹'], # Italy
    1694008: ['Republic of the Philippines', '🇵🇭'], # Philipines
    2921044: ['Deutschland', '🇩🇪'], # Germany
    2750405: ['The Netherlands'], # Netherlands
    3508796: ['República Dominicana', 'Republica Dominicana'], # Dominiucal Republic
    3932488: ['Perú', '🇵🇪'], # Peru
    1269750: ['भारत', '🇮🇳'], # India
    2802361: ['Belgique', 'België', '🇧🇪'], # Belgium 
    2260494: ['République Démocratique Du Con'], # Congo
    3996063: ['méxico', '🇲🇽'], # Mexico
    1567903: ['việt nam'], # Vietnam
    6251999: ['🇨🇦'], # Canada
    2328926: ['Nig', '🇳🇬'], # Nigeria
    3865483: ['🇦🇷'], # Argentina
    953987: ['🇿🇦'], # South Africa
    3017382: ['🇫🇷'], # France
    2300660: ['🇬🇭'], # Ghana
    1819730: ['🇭🇰'], # Hong Kong
    3895114: ['🇨🇱'], # Chile
    3686110: ['🇨🇴'], # Colombia
    1643084: ['Indone', '🇮🇩'], # Indonesia
    3625428: ['🇻🇪'], # Venezuela
    3489940: ['🇯🇲'], # Jamaica
    2077456: ['🇦🇺'], # Australia
    192950: ['🇰🇪'], # Kenya
    2658434: ['Suisse', 'Schweiz', '🇨🇭'], # Switzerland
    4566966: ['🇵🇷'], # Puerto Rico
    1168579: ['🇵🇰'], # Pakistan
    1880251: ['🇸🇬'], # Singapore
    1605651: ['ประเทศไทย'], # Thailand
    2782113: ['Österreich'], # Austria
    798544: ['Polska'], # Poland
    2287781: ["Côte d'Ivoire"], # Ivory Coast
    2287781: ['Kingdom of Saudi Arabia', 'ٱلْمَمْلَكَة ٱلْعَرَبِيَّة ٱلسَّعُوْدِيَّة'], # Saudi Arabia
    2017370: ['Россия'], # Russia
    1835841: ['Republic of Korea'], # South Korea
    2661886: ['Sverige'], # Sweden
    1814991: ["People's Republic of China"], # China
    6290252: ['Republic of Serbia'], # Serbia
    130758: ['Islamic Republic of Iran'], # Iran
    2589581: ['Algérie'], # Algeria
    3077311: ['Czech Republic'], # Czech Republic
    2464461: ['Tunisie'], # Tunisia
    290557: ['UAE'], # United Arab Emirates
    690791: ['Украина'], # Ukraine
}


""" Admin1 alternatives
"""

ALT_ADMIN1_NAMES = {
    3117732: ['Comunidad de Madrid'],
    3336901: ['Catalunya', 'Cataluña'], # Catalonia, Spain
    5332921: ['Southern California', 'SoCal'], # California, USA
    4155751: ['South Florida'], # Florida, USA
    3170831: ['Piemonte'], # Italy
    3174976: ['Lazio'],
    3174618: ['Lombardia'],
    3177401: ['Emilia Romagna'],
    3165361: ['Toscana'],
    1642672: ['Jawa Barat'], # West Java
    1642668: ['Jawa Timur'], # East Java
    2951839: ['Bayern'], # Bavaria, Germany
}


""" Discard specific 'tweet_user_location' strings
"""

LOCATION_DISCARD = ['', 'none', '\\n', 'global', 'earth',
                    'planet earth', 'worldwide', 'everywhere',
                    'internet', 'en todas partes',
                    'europe', 'africa',
                    'world', 'mars', 'text resist to 50409', 'she/her',
                    'JDSupra.com', 'Here', 'The World', 'Rock Planet', 'Somewhere',
                    'Hell', 'World Wide', 'Hogwarts', 'Neverland', 'International',
                    '127.0.0.1', 'Wakanda', 'Planeta Tierra', 'Universe', 'Heaven',
                    'Online', 'World Wide Web', 'Somewhere over the rainbow', 'Parts Unknown',
                    'Mundo', 'Narnia', 'Twitter', 'some place', 'Gotham City', 'Mother Earth',
                    'nowhere', 'nationwide', 'they/them', 'space', '#DV #CSA #Daniel_Morgan']


""" 'As-is' inputs
Set the geonameid manually of certain entries of 'tweet_user_location'
"""

AS_IS_LOCATIONS = {
    "Caracas - Venezuela": 3640847,
    "日本 東京": 1850144, # Tokyo
    "México, D.F.": 3527646,
    "México, DF": 3527646,
    "México DF": 3527646,
    "Caracas, Distrito Capital": 3640847,
    "London UK": 2643741,
    "Kuala Lumpur Federal Territory": 1733046,
    "CDMX": 3527646,
    "Ciudad Autónoma de Buenos Aire": 690791,
    "Jakarta Capital Region": 1642911,
    "San Francisco Bay Area": 5391959,
    "Bay Area": 5391959,
    "Côte d'Ivoire": 2287781,
    "Madrid, Comunidad de Madrid": 3117732, 
}