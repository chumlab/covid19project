#! /bin/bash

# cities
curl https://download.geonames.org/export/dump/cities1000.zip -o cities1000.zip
unzip cities1000.zip
rm cities1000.zip

# countries
curl https://download.geonames.org/export/dump/countryInfo.txt -o countryInfo.txt

# admin1
curl https://download.geonames.org/export/dump/admin1CodesASCII.txt -o admin1CodesASCII.txt