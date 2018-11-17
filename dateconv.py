#!/usr/bin/env python3
#to make ^ work, type './' before start of python
#======================================================================================================================
#Native Python Implementation of timevalues.f90 code
#======================================================================================================================

import argparse
from datetime import datetime
import pprint
import pandas as pd
import astropy.time as astrotime
from timevalues import time_in2time_astrotime, astrotime2time_out, input_format_guesser
pd.set_option('display.max_columns', 1000)

#Create the command line parser bit
parser = argparse.ArgumentParser(description='Creates Timevalues Based on Date Inputs', prefix_chars='-+sydjmtSYDJMT')

#Create IO arguments
parser.add_argument('-bh', '--better_help', action='store_true', help='More help information on formats etc.')

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

if __name__ == '__main__':
    #Outputs extended help function explaining all date/time formats
    if args.better_help:
        format_help_list = [         ['mjd / MJD', 'Modified Julian Date', '5 digit number', '58379.5'],
                                     ['jd / JD', 'Julian Date', '7 digit number', '2458380.0'],
                                     ['doy / DOY', 'Day Of Year', 'Day of the current year as counted from Jan 1st', '261.5'],
                                     ['yyd / YYD', 'Year Year Day of year', '2 digit year followed by day of year (day must contain 3 digits)', '18261.5 (or 18007.5)'],
                                     ['ymd / YMD', 'Year Month Day', 'year-month-day-hour-min-sec', '20180918130116.7' ],
                                     ['yymd / yymd', 'TO BE COMPLETED', 'TO BE COMPLETED'],
                                     ['str / STR', 'String Format', 'N/A', '"2019-09-18 13:01:16.742 UTC"']]
        format_help_dataframe = pd.DataFrame(format_help_list)
        pprint.pprint(format_help_dataframe)

    else:

        #Set up if statements for the time input formats and (if necessary) convert to format astropy can understand
        # checks if all input formats are false, if they are there was no input format given)
        all_inputs = [args.mjd_in, args.jd_in, args.doy_in, args.yyd_in, args.yyd_in, args.ymd_in, args.str_in, args.time_in]
        #if no input given, taken current time
        if all(x == None for x in all_inputs):
            input_format = 'mjd'
            now_time = datetime.now()
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
            print(t_out)

        elif args.jd_out:
            t_out_f = 'jd'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            print(t_out)

        elif args.doy_out:
            t_out_f = 'doy'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            print(t_out)

        elif args.yyd_out:
            t_out_f = 'yyd'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            print(t_out)

        elif args.ymd_out:
            t_out_f = 'ymd'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            print(t_out)

        elif args.str_out:
            t_out_f = 'str'
            t_out = astrotime2time_out(time_astro, time_out_format=t_out_f)
            print(t_out)


        else:
            print('unknown output format. make exception handler here?')



