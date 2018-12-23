#!/usr/bin/env python3
#to make ^ work, type './' before start of python
#======================================================================================================================
#Native Python Implementation of timevalues.f90 code
#======================================================================================================================

import pandas as pd
import argparse
from timevalues import time_in2time_astrotime, astrotime2time_out, input_format_guesser, set_argparsers, do_dateconv

pd.set_option('display.max_columns', 1000)

args = set_argparsers()
if args.noprint == True:
    printing = False
else:
    printing = True

do_dateconv(args, printing=printing)