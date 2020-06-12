# COVID-19 Project

## Geo-matching:
- match user-entered locations with a standardized geographic name
- e.g. "London", "LDN", "Lndon, England" --> "London, England", but "London, Ontario", "London Ontario", "London Canada" -- > "London, Canada"
- *possibility*: mapping from 1-dimension to 3-dimensions (City, Province/State, Country)
- e.g. "London" --> (London, N/A, England), "London, Ontario" --> "(London, Ontario, Canada)
- *alternatively*: mapping to longitude/latitude given by geonames
