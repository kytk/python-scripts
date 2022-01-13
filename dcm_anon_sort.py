#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DICOM sorting script using pydicom with anonymization
# Part of this script is based on the script written by Yuya Saito

# 26 Nov 2021 K. Nemoto
 
import sys, os, time, re, shutil, argparse, subprocess
import pydicom
 
__version__ = '0.91 (2021/11/26)'
 
__desc__ = '''
sort dicom files with anonimyzation
'''
__epilog__ = '''
examples:
  dcm_anon_sort.py DICOM_DIR
'''

def anonymize_info():
    # ID
    print("Enter ID:")
    patient_id = str(input())
    # Age
    print("Enter Age")
    temp_age = input()
    patient_age = str(temp_age.zfill(3) + "Y")
    # Birth Year
    print("Enter BirthYear: e.g. 1970")
    patient_birthyear = input()
    patient_birthdate = str(patient_birthyear + "0101")
    # Gender
    print("Enter Gender(M/F)")
    patient_sex = input().upper()
    return (patient_id, patient_age, patient_birthdate, patient_sex)
 
def generate_dest_dir_name(dicom_dataset, rule):
    if rule == 'SeriesDescription':
        rule_text = dicom_dataset.SeriesDescription.replace(' ','_')
    elif rule == 'InstanceCreatorUID':
        rule_text = dicom_dataset.InstanceCreatorUID
    elif rule == 'SeriesTime':
        rule_text = dicom_dataset.SerieseTime
    return re.sub(r'[\\|/|:|?|"|<|>|\|]|\*', '', rule_text)
 
def copy_dicom_files(src_dir, rule):
    dir_names = []
 
    # copy files
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
                dest_dir_name = generate_dest_dir_name(dataset, rule)
                out_dir = patient_id + '_anonymized'
                dest_dir = os.path.join(out_dir, dest_dir_name)
                dir_names.append(dest_dir_name)
                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, file)
                dataset.save_as(dest_file, write_like_original=False)
                #shutil.copy2(dest_file, dest_dir)
                print("anonymize %s -> %s" % (src_file, dest_file))
            except:
                pass
 
if __name__ == '__main__':
    start_time = time.time()
    parser = argparse.ArgumentParser(description=__desc__, epilog=__epilog__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('dirs', metavar='DICOM_DIR', help='DICOM directory.', nargs=1)
    parser.add_argument('-r', '--rule', metavar='RULE', default='SeriesDescription', help='classification rule. deafult SeriesDescription')
    #parser.add_argument('-o', '--out', metavar='OUT_DIR', default='.', help='output directory. default: CWD')
 
    err = 0
    try:
        args = parser.parse_args()
        patient_id, patient_age, patient_birthdate, patient_sex = anonymize_info()
        #copy_dicom_files(args.dirs[0], args.out, args.rule)
        copy_dicom_files(args.dirs[0], args.rule)
        print("execution time: %.2f second." % (time.time() - start_time))
    except Exception as e:
        print("%s: error: %s" % (__file__, str(e)))
        err = 1
 
    sys.exit(err)
