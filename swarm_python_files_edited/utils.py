import subprocess
import os
from pathlib import Path
import pandas as pd
import argparse
from datetime import datetime

# Note that function in here labelled 'ghost' also work for the process_dnsxpod_l2.py script

this_dir = os.getcwd()
top_dir = Path(this_dir).parent
dateconv_dir = os.path.join(top_dir, 'dateconv')

# Function to simplify some of the dateconv calling. Shouldnt need to change dateconv_dir but the option is there
def do_dateconv_ghost(arg, dateconv_dir=dateconv_dir):
    # takes only the input part of dateconv, everything else is automatic
    arg = [arg]
    dateconv_base = subprocess.Popen(['python3', 'dateconv.py']+arg+['+str'], cwd=dateconv_dir, stdout=subprocess.PIPE)
    # print(dateconv_base)
    dateconv_out = dateconv_base.communicate()[0].decode('utf-8')
    # print(dateconv_out, 'hh')
    panda_out = pd.to_datetime(dateconv_out)

    return panda_out


def set_argparse_ghost():
    #Create the command line parser bit
    parser = argparse.ArgumentParser(description='Exports Ghost attitude based on input time', prefix_chars='-+sydjmtfSYDJMTF01')

    #Create Input arguments
    parser.add_argument('t0=', 'T0=', '--time_in_0',  dest='time_in_0', required=False, help='Start time')
    parser.add_argument('t1=', 'T1=', '--time_in_1',  dest='time_in_1', required=False, help='End time')
    parser.add_argument('f=', 'F=', '--time_format', dest='time_f', required=False, help='Time input format (same for both)')
    parser.add_argument('-p', '--print', dest='printing', required=False, help='Prints some extra information as header', action='store_true')

    args = parser.parse_args()
    return args

def default_ghost_times():
    tnow = pd.to_datetime(datetime.now())
    t3dago = tnow - pd.to_timedelta(3, 'D')
    t1_str = str(t3dago) + " UTC"
    t10dago = tnow - pd.to_timedelta(10, 'D')
    t0_str = str(t10dago) + " UTC"
    return t0_str, t1_str

def get_panda_ghost_times():
    # Inputs need to be either both or none. if both will run from t0 to t1, if none will run for 1 week starting 10 days ago
    args = set_argparse_ghost()
    t0 = args.time_in_0
    t1 = args.time_in_1
    t_format = args.time_f
    printing = args.printing

    # do_dateconv_ghost("str=2018-12-20 17:35:11.379233 UTC")

    # Set input format for dateconv
    if t_format == None:
        if printing: print("guess format")
        dateconv_format = "t="
    else:
        if printing: print("explicit format")
        dateconv_format = "%s=" %t_format

    if t0!=None and t1!=None:
        if printing: print("Both inputs given")
        t0_dateconv_arg = dateconv_format + t0
        t1_dateconv_arg = dateconv_format + t1

    elif t0==None and t1==None:
        if printing: print("No inputs given")
        t0_str, t1_str = default_ghost_times()
        t0_dateconv_arg = 'str=%s' %t0_str
        t1_dateconv_arg = 'str=%s' %t1_str

    else:
        print("Incorrect combination of time inputs given. List as either both or none")


    # print(t0_dateconv_arg)
    # print(t0_dateconv_arg)
    t0_pd = do_dateconv_ghost(t0_dateconv_arg)
    t1_pd = do_dateconv_ghost(t1_dateconv_arg)

    return t0_pd, t1_pd
