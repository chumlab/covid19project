from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv


# 70 is an arbitrary number at the moment, will be changed accordingly (A1)
SIMPLE_RATIO_THRESHOLD = 70

with open('attempt.csv', 'w', newline='') as csvfile:
    writeLine = csv.writer(csvfile, delimiter=(
        "\t"), quotechar='|', quoting=csv.QUOTE_MINIMAL)
    with open("locations_clean_user_location.tsv", newline='', encoding="utf8") as inputFile:

        # reading first line avoid reading field names as input
        inputFile.readline()

        # read and tag countries with the geonameIDs

        reader = csv.reader(inputFile, delimiter='\t')
        for line in reader:

            # clean data (A2)
            if int(line[1]) < 2 or 'None' in line:
                continue
            else:
                with open("cities1000.txt", "r", encoding="utf8") as cityFile:
                    for cityLine in cityFile:

                        # split each column
                        cityLine = cityLine.split("\t")

                        # perform first fuzzy ratio against city name from cities1000.txt
                        value = fuzz.ratio(line[0], cityLine[1])

                        if value >= SIMPLE_RATIO_THRESHOLD:

                            # write geonameID, city name, latitude, longitude, country code
                            writeLine.writerow(
                                [cityLine[0], cityLine[2], cityLine[4], cityLine[5], cityLine[8]])

                        # if less than threshold, try next column (ASCII name)
                        else:

                            value = fuzz.ratio(line[0], cityLine[2])
                            if value >= SIMPLE_RATIO_THRESHOLD:
                                writeLine.writerow(
                                    [cityLine[0], cityLine[2], cityLine[4], cityLine[5]])

                            # if still less than threshold, try against all alternate names
                            # using process
                            else:

                                alternate_names = cityLine[3].split(",")

                                # highest match automatically becomes first element in list (A3)
                                alternate_name_ratios = process.extract(
                                    line[0], alternate_names)

                                # Check if higher than threshold
                                if alternate_name_ratios[0][1] > SIMPLE_RATIO_THRESHOLD:
                                    writeLine.writerow(
                                        [cityLine[0], cityLine[2], cityLine[4], cityLine[5], cityLine[8]])

                                # If nothing above works, check value against country info
                                # else:
                                #     with open("countryInfo.txt", "r", encoding="utf8") as countryFile:
                                #         for countryLine in countryFile:
                                #             countryLine = countryLine.split("\t")
                                #             value = fuzz.ratio(line[0], countryLine[4])
                                #             if value >= SIMPLE_RATIO_THRESHOLD:
                                #                 writeLine.writerow(
                                #                     [cityLine[0], cityLine[2], cityLine[4], cityLine[5]])
                                #                 continue
                                #             else:
                                #                 continue


'''

TODO:

A1 - Determine good threshold for simple ratio
A2 - Add to cleaning of data (remove emojis and only allow ASCII chracters??)
A3 - Handle ties

Additional: need to 

'''
