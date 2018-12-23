#======================================================================================================================
#Native Python Implementation of timevalues.f90 code
#======================================================================================================================
import argparse
import numpy as np
from datetime import datetime
import re
import astropy.time as astrotime
from datetime import datetime
import pprint
import pandas as pd
########################################################################################################################
# General Utils
########################################################################################################################
def set_argparsers():
    #Create the command line parser bit
    parser = argparse.ArgumentParser(description='Creates Timevalues Based on Date Inputs', prefix_chars='-+sydjmtSYDJMT')

    #Create IO arguments
    parser.add_argument('-bh', '--better_help', action='store_true', help='More help information on formats etc.')
    parser.add_argument('-np', '--noprint', action='store_true', help='Suppresses all printing in dateconv')

    #create output group
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('+mjd', '+MJD', '--mjd_out', dest='mjd_out', action='store_true')
    output_group.add_argument('+jd', '+JD',   '--jd_out',  dest='jd_out', action='store_true')
    output_group.add_argument('+doy', '+DOY', '--doy_out', dest='doy_out',  action='store_true')
    output_group.add_argument('+yyd', '+YYD', '--yyd_out', dest='yyd_out', action='store_true')
    output_group.add_argument('+ymd', '+YMD', '--ymd_out', dest='ymd_out', action='store_true')
    output_group.add_argument('+str', '+STR', '--str_out', dest='str_out', action='store_true')

    #create input group
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('mjd=', 'MJD=', '--mjd_in',  dest='mjd_in')
    input_group.add_argument('jd=', 'JD=', '--jd_in',     dest='jd_in')
    input_group.add_argument('doy=', 'DOY= ', '--doy_in', dest='doy_in')
    input_group.add_argument('yyd=', 'YYD=', '--yyd_in',  dest='yyd_in')
    input_group.add_argument('ymd=', 'YMD=', '--ymd_in',  dest='ymd_in')
    input_group.add_argument('str=', 'STR=', '--str_in',  dest='str_in')
    input_group.add_argument('t=', 'T=', '--time_in',  dest='time_in')


    args = parser.parse_args()
    return args


########################################################################################################################
# Converstion Utils
########################################################################################################################

def do_dateconv(args, printing=True):

    #Outputs extended help function explaining all date/time formats
    if args.better_help:
        format_help_list = [         ['mjd / MJD', 'Modified Julian Date', '5 digit number', '58379.5'],
                                     ['jd / JD', 'Julian Date', '7 digit number', '2458380.0'],
                                     ['doy / DOY', 'Day Of Year', 'Day of the current year as counted from Jan 1st', '261.5'],
                                     ['yyd / YYD', 'Year Year Day of year', '2 digit year followed by day of year (day must contain 3 digits)', '18261.5 (or 18007.5)'],
                                     ['ymd / YMD', 'Year Month Day', 'year-month-day-hour-min-sec', '20180918130116.7' ],
                                     ['str / STR', 'String Format', 'N/A', '"2019-09-18 13:01:16.742 UTC"']]
        format_help_dataframe = pd.DataFrame(format_help_list)
        pprint.pprint(format_help_dataframe)

    else:

        #Set up if statements for the time input formats and (if necessary) convert to format astropy can understand
        # checks if all input formats are false, if they are there was no input format given)
        all_inputs = [args.mjd_in, args.jd_in, args.doy_in, args.yyd_in, args.yyd_in, args.ymd_in, args.str_in, args.time_in]
        #if no input given, taken current time
        if all(x == None for x in all_inputs):
            t_in_f = 'mjd'
            t_in = datetime.now()
            now_time = t_in
            time_astro = astrotime.Time(now_time, format='datetime', precision=9)
            #print('Current time is %s' % now_time)

        elif args.time_in !=None:
            t_in = args.time_in
            t_in_f = input_format_guesser(t_in)
            time_astro = time_in2time_astrotime(t_in, time_in_format=t_in_f)

        elif args.mjd_in != None:
            t_in = args.mjd_in
            t_in_f = 'mjd'
            time_astro = time_in2time_astrotime(t_in, time_in_format=t_in_f)

        elif args.jd_in != None:
            t_in = args.jd_in
            t_in_f = 'jd'
            time_astro = time_in2time_astrotime(t_in, time_in_format=t_in_f)

        elif args.doy_in != None:
            t_in = args.doy_in
            t_in_f = 'doy'
            time_astro = time_in2time_astrotime(t_in, time_in_format=t_in_f)

        elif args.yyd_in != None:
            t_in = args.yyd_in
            t_in_f = 'yyd'
            time_astro = time_in2time_astrotime(t_in, time_in_format=t_in_f)

        elif args.ymd_in != None:
            t_in = args.ymd_in
            t_in_f = 'ymd'
            time_astro = time_in2time_astrotime(t_in, time_in_format=t_in_f)

        elif args.str_in != None:
            t_in = args.str_in
            t_in_f = 'str'
            time_astro = time_in2time_astrotime(t_in, time_in_format=t_in_f)



        #Set up if statements for the output conversion


        #DO FUNCTION HERE THAT LOOKS LIKE
        # doit(output_format, output_value) --> output time wanted


        #Note:mjd is standard output
        # checks if all outputs formats are false, if they are there was no output format given)
        all_outputs = [args.mjd_out, args.jd_out, args.doy_out, args.yyd_out, args.yyd_out, args.ymd_out, args.str_out]
        try:
            this = time_astro
        except NameError:
            print('"time_astro" was not defined. Check all inputs are correct.')
            exit()

        if args.mjd_out or all(x == False for x in all_outputs):
            t_out_f = 'mjd'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            # print(t_out)

        elif args.jd_out:
            t_out_f = 'jd'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            # print(t_out)

        elif args.doy_out:
            t_out_f = 'doy'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            # print(t_out)

        elif args.yyd_out:
            t_out_f = 'yyd'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            # print(t_out)

        elif args.ymd_out:
            t_out_f = 'ymd'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            # print(t_out)

        elif args.str_out:
            t_out_f = 'str'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            # print(t_out)

        else:
            t_out = 'unknown output format. make exception handler here?'

        if printing: print(t_out)

        return [t_in_f, t_in, t_out_f, t_out]

#Usually works, but some things categorised as 'mjd' could have been yyd instead
def input_format_guesser(t_in):
    try:
        t_in = np.float64(t_in)
        t_in_str = str(t_in)
        interdec_list = t_in_str.split('.')

        if len(interdec_list) == 2:
            integer, decimal = interdec_list
        elif len(interdec_list) == 1:
            integer, decimal = interdec_list[0], '0'

        if t_in_str[-3:] == 'UTC':
            format = 'str'

        elif (len(integer) == 14) and (int(integer[0:4]) in range(1950,2050)):
            format = 'ymd'

        elif 2433282 < t_in < 2469807.5:
            format = 'jd'

        elif 33282 < t_in < 69807:
            format = 'mjd'

        else:
            format = 'yyd'
    except ValueError:
        print('Unknown input. Try specifying the format. \nMust be one of following: mjd, jd, yyd, ymd, str. \nUse -bh if you need more help on formats')
        exit()
    except NameError:
        print('"integer" was not defined. Check time input, and if still not working make sure the input is decimal.')
        exit()


    return format

#function to take time in, time format in, and convert to an astropy time object. mjd is standard input
def time_in2time_astrotime(time_in, time_in_format='mjd'):

    #Set precision (number of DP) to use in astropy objects
    precis = 9

    if time_in_format == 'mjd':
        mjd_time = np.float64(time_in)
        mjd_time_astro = astrotime.Time(mjd_time, format='mjd', precision=precis)
        return mjd_time_astro


    elif time_in_format == 'jd':
        jd_time = np.float64(time_in)
        jd_time_astro = astrotime.Time(jd_time, format='jd', precision=precis)
        return jd_time_astro

    elif time_in_format == 'doy':
        doy_time = np.float64(time_in)
        print('I dont know the year so I cant do anything with this')

    elif time_in_format == 'yyd':
        yyd_time_str = str(time_in)

        #define year, day and decimal portion from input string
        interdec_list = yyd_time_str.split('.')
        if len(interdec_list) == 2:
            integer, decimal = interdec_list
        elif len(interdec_list) == 1:
            integer, decimal = interdec_list[0], '0'
        try:
            year_str = integer[0:2]
        except NameError:
            print('"integer" was not defined. Check time input, and if still not working make sure the input is decimal.')
            exit()
        day_str = integer[2:]
        try:
            decimal = np.float64('0.'+decimal)
        except NameError:
            print('"decimal" was not defined. Check time input, and if still not working make sure the input is decimal.')
            exit()

        #create hours minutes and seconds portions of date, convert to correct format for astropy
        hours = decimal*24
        hours_str = str(int(hours))
        minutes = (hours%1)*60
        minutes_str = str(int(minutes))
        seconds = (minutes%1)*60
        seconds_str = str(seconds)

        #set century and create full year string
        if 55 <= int(year_str)  <= 99:
            century_prefix = '19'
        elif 0 <= int(year_str) <= 50:
            century_prefix = '20'
        try:
            year_full_str = century_prefix + year_str
        except NameError:
            print('"century_prefix" was not defined. Check time input, and if still not working make sure the input is decimal.')
            exit()

        #create astropy input string, and create astropy time
        yyd_time_astrostr = '%s:%s:%s:%s:%s' % (year_full_str, day_str, hours_str, minutes_str, seconds_str)
        yyd_time_astro = astrotime.Time(yyd_time_astrostr, format='yday', precision=precis)
        return yyd_time_astro

    elif time_in_format == 'ymd':
        ymd_time_str = str(time_in)

        #create year, month etc strings
        year_str = ymd_time_str[0:4]
        month_str = ymd_time_str[4:6]
        day_str = ymd_time_str[6:8]
        hours_str = ymd_time_str[8:10]
        minutes_str = ymd_time_str[10:12]
        seconds_str = ymd_time_str[12:]

        #create full string to pass to astro
        ymd_time_astrostr = '%s-%s-%s %s:%s:%s' % (year_str, month_str, day_str, hours_str, minutes_str, seconds_str)

        #create astrotime object
        ymd_time_astro = astrotime.Time(ymd_time_astrostr, format='iso', precision=precis)
        return ymd_time_astro

    elif time_in_format == 'str':
        #Trime the UTC from original string
        str_time = str(time_in[:-4])
        #create astropy object
        str_time_astro = astrotime.Time(str_time, format='iso', precision=precis)
        return str_time_astro





def astrotime2time_out(time_in, time_out_format='mjd'):

    #EXCEPTION HANDLER FOR NON-ASTROPY OBJECTS NEEDED

    # Set up if statements for the output conversion

    if time_out_format == 'mjd':

        time_astr_mjd = time_in
        time_astr_mjd.format = 'mjd'
        return np.float64(str(time_astr_mjd))


    elif time_out_format == 'jd':
        time_astr_jd = time_in
        time_astr_jd.format = 'jd'
        return np.float64(str(time_astr_jd))


    #A lot of code is similar for doy or yyd, therefore group together
    elif time_out_format=='doy' or time_out_format=='yyd':
        #First convert astro time into yyd astro time, and collect a string list + float list of values
        time_in.format = 'yday'
        time_astr_yyd_str = str(time_in)
        time_astr_yyd_str_lst = time_astr_yyd_str.split(':')
        time_astr_yyd_float_lst = np.float64(time_astr_yyd_str_lst)

        #set list members as more readable variables
        year, days, hours, minutes, seconds = time_astr_yyd_float_lst

        #calculate what the hours minutes and seconds would be as a fraction of a day
        decimal_day = hours/24 + (minutes/60)/24 + ((seconds/60)/60)/24
        days_total_str = str(days + decimal_day)

        #shorten year string to proper format
        year_str = time_astr_yyd_str_lst[0]
        year_str_short = year_str[2:]

        #new if statements to do doy and yyd
        if time_out_format=='doy':
            return np.float64(str(days_total_str))

        elif time_out_format=='yyd':
            time_yyd_str = year_str_short + days_total_str
            return np.float64(str(time_yyd_str))

    elif time_out_format=='ymd':
        time_in.format = 'iso'
        time_astr_ymd_str = str(time_in)
        time_astr_ymd_str_lst = re.split('-|\s|\s|:', time_astr_ymd_str)
        time_ymd_str = ''.join(time_astr_ymd_str_lst)
        return np.float64(str(time_ymd_str))


    elif time_out_format=='str':
        time_in.format = 'iso'
        time_astr_str = str(time_in)
        time_str = time_astr_str + ' UTC'
        return str(time_str)




