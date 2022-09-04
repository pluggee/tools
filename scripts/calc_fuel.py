import csv
import os
from ourairports import OurAirports

report_filename = 'report.txt'
all_airports = OurAirports()    # pre-load from files only once
trip_fuel_threshold = 1.0
destination_search_radius = 2.0

def find_airport(latitude, longitude):
    dis_lat = destination_search_radius/69.0
    dis_long = destination_search_radius/54.6
    ret_airport = []
    for airport in all_airports.airports:
        if abs(float(airport.latitude) - float(latitude)) < dis_lat:
            if abs(float(airport.longitude) - float(longitude)) < dis_long:
                if 'airport' in airport.type:
                    ret_airport = airport
                    break
    return airport


def get_from_file(filename):
    ff_col = 0
    long_col = 0
    lat_col = 0
    total_fuel = 0
    last_long = ''
    last_lat = ''
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        ff_check = False
        long_check = False
        lat_check = False
        skip_col_check = False
        for row in reader:
            if (len(row) > 80):
                if not skip_col_check:
                    c_col = 0
                    for h in row:
                        if 'FFlow' in h:
                            ff_col = c_col
                            ff_check = True
                        if 'Longitude' in h:
                            long_col = c_col
                            long_check = True
                        if 'Latitude' in h:
                            lat_col = c_col
                            lat_check = True
                        c_col += 1
                        if ff_check:
                            if long_check:
                                if lat_check:
                                    skip_col_check = True
                else:
                    # calculating fuel flow
                    try:
                        total_fuel += float(row[ff_col])/3600
                    except:
                        pass
                    last_lat = row[lat_col]
                    last_long = row[long_col]
    return total_fuel, last_lat, last_long

file_list = os.listdir(".")
file_list.sort()

total_fuel = 0

with open(report_filename, 'w') as repfile:
    header = 'Origin' + ' ➜ ' + 'Dest  ' + ' | ' + 'TO Date     ' + ' | ' + 'TO Time   ' + ' | ' + ' Fuel '
    print(header)
    repfile.write(header)
    repfile.write('\n')
    header = '------' + '---' + '------' + '-|-' + '------------' + '-|-' + '----------' + '-|-' + '------'
    print(header)
    repfile.write(header)
    repfile.write('\n')


    # all_airports = OurAirports()
    for filename in file_list:
        if (filename.startswith('log')):
            # print('---')
            # print(filename)
            file_details = (filename.split('.')[0]).split('_')
            # print(file_details)
            fdate = file_details[1][0:4] + '/' + file_details[1][4:6] + '/' + file_details[1][6:]
            ftime = file_details[2][0:2] + ':' + file_details[2][2:4] + ':' + file_details[2][4:]
            origin = file_details[3]
            fuel_consumption, dest_lat, dest_long = get_from_file(filename)

            if (origin == ""):
                origin = "NONE"

            if (fuel_consumption > trip_fuel_threshold):
                # only search airports if fuel consumption is above threshold
                dest_airport = find_airport(dest_lat, dest_long)
                if dest_airport:
                    destination = dest_airport.icao
                else:
                    destination = 'UNKN'
                total_fuel += fuel_consumption
                printline = origin.rjust(6) + ' ➜ ' + destination.ljust(6) + ' | '\
                    + fdate.ljust(12) + ' | ' + ftime.ljust(10) + ' | ' \
                    + str(round(fuel_consumption,2)).rjust(6)
                print(printline)
                repfile.write(printline)
                repfile.write('\n')

    repfile.close()

print()
print('Total Fuel Consumption: ' + str(round(total_fuel,2)))
