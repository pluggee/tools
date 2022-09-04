import csv
import os
from ourairports import OurAirports

all_airports = OurAirports()

# total_num = 0
# for airport in all_airports:
#     total_num += 1
print('Database elements : ' + str(len(all_airports.airports)))

lat = '37.6944313'
long = '-121.8111294'

lat_f = float(lat)
long_f = float(long)

dis_lat = 1/30
dis_long = 1/25

found_airport = False
for airport in all_airports.airports:
    if abs(float(airport.latitude) - lat_f) < dis_lat:
        if abs(float(airport.longitude) - long_f) < dis_long:
            print('Found match!')
            print(airport.icao)
            break


# for filename in file_list:
#     repfile = open(report_filename, 'r')
#     if (filename not in repfile.read()):
#         # close until calculation is complete
#         repfile.close()
#         if (filename.startswith('log')):
#             # print('---')
#             # print(filename)
#             file_details = (filename.split('.')[0]).split('_')
#             # print(file_details)
#             fdate = file_details[1][0:4] + '/' + file_details[1][4:6] + '/' + file_details[1][6:]
#             ftime = file_details[2][0:2] + ':' + file_details[2][2:4] + ':' + file_details[2][4:]
#             origin = file_details[3]
#             fuel_consumption, dest_lat, dest_long = get_from_file(filename)
#
#             if (origin == ""):
#                 origin = "NONE"
#
#             if (fuel_consumption > 1.0):
#                 # only search airports if fuel consumption is above threshold
#                 dest_airports = all_airports.getAirportsByDistance(dest_lat, dest_long, 1.5)
#                 if len(dest_airports) == 0:
#                     destination = 'UNKN'
#                 else:
#                     destination = dest_airports[0].icao
#
#                 printline = origin.rjust(6) + ' ➜ ' + destination.ljust(6) + ' | '\
#                     + fdate.ljust(12) + ' | ' + ftime.ljust(10) + ' | ' \
#                     + str(round(fuel_consumption,2)).rjust(6) + ' | ' + filename
#                 print(printline)
#                 repfile = open(report_filename, 'a')
#                 repfile.write(printline)
#                 repfile.write('\n')
#                 repfile.close()
#     else:
#         # cleanup
#         print('Found file ' + filename + ' in report, skipping ...')
#         repfile.close()
