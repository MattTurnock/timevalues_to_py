#!/usr/bin/env python3
import zipfile
import os
import glob
import tempfile

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

satletters = ["A", "B", "C"]
lastdays=3

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
