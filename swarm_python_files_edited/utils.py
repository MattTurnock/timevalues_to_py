import subprocess
import os
from pathlib import Path
import pandas as pd
import argparse

this_dir = os.getcwd()
top_dir = Path(this_dir).parent
dateconv_dir = os.path.join(top_dir, 'dateconv')

# Function to simplify some of the dateconv calling. Shouldnt need to change dateconv_dir but the option is there
def do_dateconv_ghost(arg, dateconv_dir=dateconv_dir):
    # takes only the input part of dateconv, everything else is automatic
    arg = [arg]
    dateconv_base = subprocess.Popen(['python3', 'dateconv.py']+arg+['+str'], cwd=dateconv_dir, stdout=subprocess.PIPE)
    dateconv_out = dateconv_base.communicate()[0].decode('utf-8')
    panda_out = pd.to_datetime(dateconv_out)

    return panda_out

#Create the command line parser bit
parser = argparse.ArgumentParser(description='Exports Ghost attitude based on input time', prefix_chars='-+sydjmtSYDJMT')

#Create IO arguments


#create output group
# output_group = parser.add_mutually_exclusive_group()
# output_group.add_argument('+mjd', '+MJD', '--mjd_out', dest='mjd_out', action='store_true')
# output_group.add_argument('+jd', '+JD',   '--jd_out',  dest='jd_out', action='store_true')
# output_group.add_argument('+doy', '+DOY', '--doy_out', dest='doy_out',  action='store_true')
# output_group.add_argument('+yyd', '+YYD', '--yyd_out', dest='yyd_out', action='store_true')
# output_group.add_argument('+ymd', '+YMD', '--ymd_out', dest='ymd_out', action='store_true')
# output_group.add_argument('+str', '+STR', '--str_out', dest='str_out', action='store_true')

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
