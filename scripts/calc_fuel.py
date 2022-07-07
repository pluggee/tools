import csv
import os

def calc_fuel_from_file(filename):
    ff_col = 0
    total_fuel = 0
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        skip_col_check = False
        for row in reader:
            if (len(row) > 80):
                if not skip_col_check:
                    c_col = 0
                    for h in row:
                        if 'FFlow' in h:
                            ff_col = c_col
                            skip_col_check = True
                            #print('FFlow column is ' + str(ff_col))
                        else:
                            c_col += 1
                else:
                    # calculating fuel flow
                    try:
                        total_fuel += float(row[ff_col])/3600
                    except:
                        pass
    return total_fuel

file_list = os.listdir(".")
file_list.sort()

for filename in file_list:
    if (filename.startswith('log')):
        # print('---')
        # print(filename)
        file_details = (filename.split('.')[0]).split('_')
        # print(file_details)
        fdate = file_details[1][0:4] + '/' + file_details[1][4:6] + '/' + file_details[1][6:]
        ftime = file_details[2][0:2] + ':' + file_details[2][2:4] + ':' + file_details[2][4:]
        origin = file_details[3]
        fuel_consumption = calc_fuel_from_file(filename)

        if (origin == ""):
            origin = "NONE"

        if (fuel_consumption > 0.0):
            printline = origin.rjust(6) + ' | ' \
                + fdate.ljust(12) + ' | ' + ftime.ljust(10) + ' | ' \
                + str(round(fuel_consumption,2)).rjust(6)
            print(printline)


#print('Total fuel consumed = ' + str(round(calc_fuel_from_file('log_20220626_094308_KEKO.csv'),2)))
