#!/usr/bin/env python3
import os
import pandas as pd
from datetime import datetime
satletters = ["A", "B", "C"]

nrtdm_products_inorder = [
  "_Models/DensityModel_NRLMSISE-00",
  "_Models/WindModel_Local_HWM07",
  "_Models/WindModel_SC_HWM07",
  "_Panels/CFaero",
  "_Panels/Aero",
  "_Panels/Accel_AeroRadiationPressure",
  "_FAST/Accel_Calibrated_NoRadiationPressure",
  "_FAST/Density_Direct",
  "_FAST/DataFlags",
  "_FAST/Density_Direct_OrbitMean"
]

tnow = pd.to_datetime(datetime.now())
tend = tnow - pd.to_timedelta(3, 'D')
tstart = tnow - pd.to_timedelta(100, 'D')

ymd0 = datetime.strftime(tstart, '%Y%m%d000000') # Round down to midnight on the day
ymd1 = datetime.strftime(tend, '%Y%m%d000000')

timearg = f"t={ymd0},{ymd1}"

for satletter in satletters:
    for productname in nrtdm_products_inorder:
        fullproductname = f"S{satletter}{productname}"
        command = f"processdataproducts.exe {fullproductname} {timearg}"
        print(command)
        os.system(command)

