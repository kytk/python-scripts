#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DICOM anonymizing script for AMED registry
# 26 Nov 2021 K. Nemoto
 
import sys, os, time, re, argparse, subprocess
import pydicom
 
__version__ = '0.93 (2021/11/26)'
 
__desc__ = '''
anonymize(modify) dicom files
'''
__epilog__ = '''
Usage:
  dcm_anonymize DICOM_DIR
'''

def anonymize_info():
    # ID
    print("Enter ID:")
    patient_id = str(input())
    # Age
    print("Enter Age")
    patient_age = input()
    patient_age = str(patient_age.zfill(3) + "Y")
    # Birth Year
    print("Enter BirthYear: e.g. 1970")
    patient_birthyear = input()
    patient_birthdate = str(patient_birthyear + "0101")
    # Gender
    print("Enter Gender(M/F)")
    patient_sex = input().upper()
    return (patient_id, patient_age, patient_birthdate, patient_sex)

 
def anon_dicom_files(src_dir):
    # anonymize files
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            try:
                src_file = os.path.join(root, file)
                dataset = pydicom.dcmread(src_file)
                dataset.PatientName = patient_id
                dataset.PatientID = patient_id
                dataset.PatientAge = patient_age
                dataset.PatientSex = patient_sex
                dataset.PatientBirthDate = patient_birthdate
                dest_dir = patient_id + '_anonymized'
                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, file)
                print("anonymize %s -> %s" % (src_file, dest_file))
                dataset.save_as(dest_file, write_like_original=False)
            except:
                pass
 
if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser(description=__desc__, epilog=__epilog__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dirs', metavar='DICOM_DIR', help='DICOM directory.', nargs=1)
 
    err = 0
    try:
        args = parser.parse_args()
        patient_id, patient_age, patient_birthdate, patient_sex = anonymize_info()
        anon_dicom_files(args.dirs[0])
        print("execution time: %.2f second." % (time.time() - start_time))
    except Exception as e:
        print("%s: error: %s" % (__file__, str(e)))
        err = 1
 
    sys.exit(err)
