#======================================================================================================================
#Native Python Implementation of timevalues.f90 code
#======================================================================================================================

import numpy as np
from datetime import datetime
import astropy.time as astrotime
import re

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




