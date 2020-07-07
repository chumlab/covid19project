from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv


# 91 is an arbitrary number at the moment, will be changed accordingly (A1)
RATIO_THRESHOLD = 89


def read_country_info(location_name, writer):
    with open("countryinfo.txt", "r", encoding="utf8") as countryfile:
        for countryline in countryfile:
            countryline = countryline.split("\t")

            value_simple = fuzz.ratio(line[0].lower(), countryline[4].lower())

            if value_simple >= RATIO_THRESHOLD:
                print('Country found: ' + line[0] + " --> " + countryline[4])
                writer.writerow(
                    [countryline[16], countryline[4]])
                return True
            else:
                continue
        return False
    

def read_city(location_name, writer):
    with open("cities1000.txt", "r", encoding="utf8") as cityFile:
        for cityLine in cityFile:

            # split each column
            cityLine = cityLine.split("\t")

            # perform first fuzzy ratio against city name from cities1000.txt
            value_simple = fuzz.ratio(line[0].lower(), cityLine[1].lower())

            if value_simple >= RATIO_THRESHOLD:

                # write geonameID, city name, latitude, longitude, country code
                print('City found (1): ' + line[0] + " --> " + cityLine[1])
                writer.writerow( [cityLine[0], cityLine[2], cityLine[4], cityLine[5], cityLine[8]])
                return True

            # if less than threshold, try next column (ASCII name)
            else:

                value_simple = fuzz.ratio(line[0].lower(), cityLine[2].lower())
                if value_simple >= RATIO_THRESHOLD:
                    print('City found (2): ' + line[0] + " --> " + cityLine[1])
                    writer.writerow([cityLine[0], cityLine[2], cityLine[4], cityLine[5], cityLine[8]])

            #     # if still less than threshold, try against all alternate names
            #     # using process
            #     else:

            #         alternate_names = cityLine[3].split(",")
            #         alternate_names = [x.lower() for x in alternate_names]

            #         # highest match automatically becomes first element in list (A3)
            #         alternate_name_simple = process.extractOne(line[0].lower(), alternate_names, scorer = fuzz.ratio)

            #         # Check if higher than threshold
            #         if alternate_name_simple[1] >= RATIO_THRESHOLD:
            #             print(alternate_name_simple)
            #             print('City found (3): ' + line[0] + " --> " + cityLine[1])
            #             writer.writerow([cityLine[0], cityLine[2], cityLine[4], cityLine[5], cityLine[8]])
            #             return True

        return False


with open('attempt.csv', 'w', newline='') as csvfile:
    writeLine = csv.writer(csvfile, delimiter=("\t"), quotechar='|', quoting=csv.QUOTE_MINIMAL)
    with open("Full_user_location.tsv", newline='', encoding="utf8") as inputFile:

        # reading first line avoid reading field names as input
        inputFile.readline()

        # read and tag countries with the geonameIDs
        reader = csv.reader(inputFile, delimiter='\t')
        for line in reader:
        
            # line will remove anything but ascii symbols
            encoded_string = [x.encode("ascii","ignore") for x in line]
            line = [x.decode() for x in encoded_string]

            if "," in line[0]:
                line[0] = line[0].split(",")[0]

            # clean data (A2)
            if int(line[1]) < 4 or 'None' in line or 'False' in line or 'True' in line:
                continue
            else:
                if read_country_info(line[0], writeLine): 
                    continue
                elif read_city(line[0], writeLine): 
                    continue
               


                
                                    



'''

TODO:

A1 - Determine good threshold for simple ratio
A3 - Handle ties


'''
