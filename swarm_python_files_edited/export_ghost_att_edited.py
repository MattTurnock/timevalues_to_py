#!/usr/bin/env python3
################################################################################################################
# Changed functionality: now runs from command line, with following configs:
#       No arguments       - runs from t0=10 days ago to t1=3 days ago
#       t0 and t1 given    - guesses input type (mjd, ymd etc) and runs from t0 to t1
#       t0, t1 and f given - like above, but makes input format explicit (in case guessing function doesnt work)
################################################################################################################

import pandas as pd
from datetime import datetime
from utils import do_dateconv_ghost, get_panda_ghost_times

args = ['ymd=20180918130116.7', '+str']
t0_pd = do_dateconv_ghost('ymd=20180918130116.7')
print(t0_pd)


outputpath = "/home/swarmgen/WP8000/commissioning/POD/Data/Att" 
exportsettings = "-nofooter -noheader -invalid=skip -realformat=f13.10"

satletters = ["A", "B", "C"]

tnow = pd.to_datetime(datetime.now())
t3dago = tnow - pd.to_timedelta(3, 'D')
t10dago = tnow - pd.to_timedelta(10, 'D')


######################################################################################
t0_arg = 'ymd=20180918130116.7'
t1_arg = 'ymd=20180919130116.7'

# t0_pd = do_dateconv_ghost(t0_arg)
# t1_pd = do_dateconv_ghost(t1_arg)
t0_pd, t1_pd = get_panda_ghost_times()
print(t0_pd, t1_pd)

########################################################################################

ymd0 = datetime.strftime(t0_pd, '%Y%m%d000000') # Round down to midnight on the day
ymd1 = datetime.strftime(t1_pd, '%Y%m%d000000')

t0 = pd.to_datetime(ymd0)
t1 = pd.to_datetime(ymd1)

year = t0.year
doy = t0.dayofyear

daystarts = pd.DatetimeIndex(freq='1D', start=t0, end=t1)
print(daystarts)

for daystart in daystarts:
    dayend = daystart + pd.to_timedelta(1, 'D')
    ymd0 = datetime.strftime(daystart, '%Y%m%d')
    ymd1 = datetime.strftime(dayend, '%Y%m%d')
    year = daystart.year
    doy = daystart.dayofyear 
    for satletter in satletters:
        productlist = ""
        for quatfield in ["4", "1", "2", "3"]:
            productlist += f"S{satletter}_Basic/Quat_Interpolated/{quatfield} " 
        command = f"exportdataproductscdf.exe {exportsettings} {productlist} -timeformat=gho t=gps:{ymd0},{ymd1} > {outputpath}/S{satletter}_{year}_{doy}.att"
        print(command)
        #os.system(command)
