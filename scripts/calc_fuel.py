import csv
import os
from ourairports import OurAirports

report_filename = 'report.txt'

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

# check if report file exists
if (os.path.exists(report_filename)):
    print('report file exists')
else:
    print('report file does not exist, creating ...')
    with open(report_filename, 'w') as f:
        header = 'Origin' + ' ➜ ' + 'Dest  ' + ' | ' + 'TO Date     ' + ' | ' + 'TO Time   ' + ' | ' + ' Fuel ' + ' | Filename'
        print(header)
        f.write(header)
        f.write('\n')
        f.close()

all_airports = OurAirports()
for filename in file_list:
    repfile = open(report_filename, 'r')
    if (filename not in repfile.read()):
        # close until calculation is complete
        repfile.close()
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

            if (fuel_consumption > 1.0):
                # only search airports if fuel consumption is above threshold
                dest_airports = all_airports.getAirportsByDistance(dest_lat, dest_long, 1.5)
                if len(dest_airports) == 0:
                    destination = 'UNKN'
                else:
                    destination = dest_airports[0].icao

                printline = origin.rjust(6) + ' ➜ ' + destination.ljust(6) + ' | '\
                    + fdate.ljust(12) + ' | ' + ftime.ljust(10) + ' | ' \
                    + str(round(fuel_consumption,2)).rjust(6) + ' | ' + filename
                print(printline)
                repfile = open(report_filename, 'a')
                repfile.write(printline)
                repfile.write('\n')
                repfile.close()
    else:
        # cleanup
        print('Found file ' + filename + ' in report, skipping ...')
        repfile.close()
