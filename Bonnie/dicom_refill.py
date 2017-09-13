# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime
import pandas as pd
import dicom


# Global variables
DICOM_PATTERN = r'^IM[G]?-[0-9]{4}-[0-9]{4}.dcm$'
HOME_DIR = "C:\\Users\\LKT\\Documents\\PythonProject\\FirstProj\\testing"
LOG_FILE = "C:\\Users\\LKT\\Documents\\PythonProject\\FirstProj\\log.txt"

# Function to write log
def write_log(log_file, msg):
    with open(log_file, 'a') as f:
        f.write("%s: %s\n" % (datetime.now(), msg))


# Function to refill full name and full id for a dicom image
def dicom_refill(img_path, full_name, full_id):
    img = dicom.read_file(img_path)
    img[0x10, 0x10].value = '^'.join(full_name.split(', '))
    img[0x10, 0x20].value = full_id
    img.save_as(img_path)
    return None


# Function to loop through directories and search for dicom images
def loop_dir(parent_dir, current_file_name):
    write_log(LOG_FILE, "Looking at %s" % parent_dir)
    
    if not os.path.exists(parent_dir):
        write_log(LOG_FILE, "Directory does not exists: %s" % parent_dir)
        return None
    
    count_dicom, count_non_dicom = 0, 0
    for item in os.listdir(parent_dir):
        this_path = os.path.join(parent_dir, item)
        
        # Continue to search if this_path is a directory, refill otherwise
        if os.path.isdir(this_path):
            loop_dir(this_path, current_file_name)
        else:
            if bool(re.match(DICOM_PATTERN, item)):
                patient_name = STR_list.Dicom_Name[STR_list.File_Name == current_file_name].tolist()[0]
                patient_id = STR_list.Dicom_ID[STR_list.File_Name == current_file_name].tolist()[0]
                dicom_refill(this_path, patient_name, patient_id)
                count_dicom += 1
            else:
                write_log(LOG_FILE, "Non-dicom pattern file name found: %s" % this_path)
                count_non_dicom += 1
    
    write_log(LOG_FILE,
              "Summary: In %s, refilled %s DICOM images, %s non-DICOM images found" % (parent_dir, count_dicom, count_non_dicom))


# Read in subject list
STR_list = pd.read_csv("C:\\Users\\LKT\\Documents\\PythonProject\\FirstProj\\stride_subject_list.txt", sep='\t', header=0)

# Loop through File_Name in STR_list
for file_name in STR_list.File_Name:
    loop_dir(os.path.join(HOME_DIR, file_name), file_name)
