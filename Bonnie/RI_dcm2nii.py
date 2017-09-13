# -*- coding: utf-8 -*-
import os
from datetime import datetime


# Global variables
HOME_DIR = "/Volumes/Share/Imaging_Archive/Risk_Index/MRI/dicom_original"
OUT_NAME = "/Volumes/Share/Imaging_Archive/Risk_Index/MRI/niftii/%s/%s_1/%s_T1.nii"
LOG_FILE = "/Users/Bonnie/Desktop/log.txt"

# Function to write log
def write_log(log_file, msg):
    with open(log_file, 'a') as f:
        f.write("%s: %s\n" % (datetime.now(), msg))


with open("List_T1_dicom_2_nifti.txt", 'r') as f:
    RI_list = f.readlines()

# Replace '\n' in RI_list
RI_list = [_.replace('\n', '') for _ in RI_list]

# Loop for each RI number
for RI_no in RI_list:
    write_log(LOG_FILE, "Working on %s" % RI_no)
    
    # Search for directory
    full_dir = os.path.join(HOME_DIR, RI_no, RI_no + "_1", "T1_AX", "DICOM")
    if os.path.exists(full_dir):
        dcm2nii = "dcm2nii"
        os.system(dcm2nii)
        os.rename("old_name", OUT_NAME % (RI_no, RI_no, RI_no))
    else:
        write_log(LOG_FILE, "Error: cannot find T1_AX director for %s" % RI_no)
