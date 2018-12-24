#!/usr/bin/env python3
################################################################################################################
# Changed functionality: now runs from command line, allowing any number of lastdays BUT:
#       Not sure how the file structure works (no access to hpfa) therefore dateconv not implemented for custom
#       dates yet
#       Lastdays is 3 if not specified
################################################################################################################

import zipfile
import os
import glob
import tempfile
import argparse

def import_to_nrtdm(filelist, l1b_ext, nrtdm_product):
    with tempfile.TemporaryDirectory() as tmpdirpath:
        for filename in filelist:
            zip_archive = zipfile.ZipFile(filename)
            for file_in_zip in zip_archive.namelist():
                basename, extension = os.path.splitext(file_in_zip)
                if extension == l1b_ext:
                    extracted_file = zip_archive.extract(file_in_zip, tmpdirpath)
                    command = f"importdataproducts.exe {nrtdm_product} -in-file={extracted_file}"
                    print(command)
                    os.system(command)

# Argument parser to get lastdays
parser = argparse.ArgumentParser(description='Exports commands for nrtdm based on number of previous days', prefix_chars='-+ls')
parser.add_argument('ls=', '--lastdays', type=int, dest='lastdays', required=False, help='Number of previous days')
parser.add_argument('-p', '--print', dest='printing', required=False, help='Prints some extra information as header', action='store_true')
args = parser.parse_args()
lastdays_arg = args.lastdays
printing = args.printing
if lastdays_arg == None:
    lastdays=3
else:
    lastdays = lastdays_arg

if printing: print("Last days taken: %s" %lastdays)

satletters = ["A", "B", "C"]
# lastdays=3

nrtdm_products_inputs = {
  "MODx_SC": ["Orbit_L1B"], 
  "STRxATT": ["Quat_L1B", "Quat_Flags_L1B"],
  "SC_xDYN": ["SpacecraftMass_L1B"],
}
producttypes = nrtdm_products_inputs.keys()

l1b_base_path = "/hpfa/swarmgen/Level1b/Latest_baselines"

l1b_exts = {
  "MODx_SC": ".sp3",
  "STRxATT": ".cdf",
  "SC_xDYN": ".cdf"
}

for satletter in satletters:
    for producttype in producttypes:
        l1b_path = f"{l1b_base_path}/{producttype}/Sat_{satletter}/"
        filelist = glob.glob(l1b_path + '/*.ZIP')
        reducedfilelist = filelist[-lastdays:] # Take last x files only TODO: implement date check
        for nrtdm_products_input in nrtdm_products_inputs[producttype]:
            nrtdm_product = f"S{satletter}_Basic/{nrtdm_products_input}"
            import_to_nrtdm(reducedfilelist, l1b_exts[producttype], nrtdm_product)
