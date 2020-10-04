#! /bin/bash

# The following datasets are expected:

# * `cities1000.tsv`, cities with > 1000 pop. (GeoNames):
#   * https://download.geonames.org/export/dump/cities1000.zip
#   * Unzipped and renamed to `.tsv`
# * `countryInfo.tsv`, countries (GeoNames):
#   * https://download.geonames.org/export/dump/countryInfo.txt
#   * Unzipped and renamed to `.tsv`
# * `admin1CodesASCII.txt`, states and provinces (admin1) (GeoNames)
#   * https://download.geonames.org/export/dump/admin1CodesASCII.txt

# cities
curl https://download.geonames.org/export/dump/cities1000.zip -o cities1000.zip
unzip cities1000.zip
rm cities1000.zip

curl https://download.geonames.org/export/dump/countryInfo.txt -o countryInfo.txt
curl https://download.geonames.org/export/dump/admin1CodesASCII.txt -o admin1CodesASCII.txt