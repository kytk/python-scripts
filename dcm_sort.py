#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DICOM sorting script using pydicom
# Part of this script is based on the script provided by Yuya Saito

# 07 Aug 2022 K. Nemoto
 
import sys, os, time, re, shutil, argparse, subprocess
import pydicom
 
__version__ = '1.2 (2022/08/07)'
 
__desc__ = '''
sort dicom files.
'''
__epilog__ = '''
examples:
  dcm_sort.py DICOM_DIR
'''

def generate_dest_dir_name(dicom_dataset):
    seriesnumber = str(dicom_dataset.SeriesNumber).zfill(2)
    seriesdescrip = dicom_dataset.SeriesDescription.replace(' ','_')
    rule_text = '{}_{}'.format(seriesnumber, seriesdescrip) 
    return re.sub(r'[\\|/|:|?|"|<|>|\|]|\*', '', rule_text)

def copy_dicom_files(src_dir):
    # make a directory "sorted" if it doesn't exist
    dir_names = []
    if not os.path.exists('sorted'):
        os.makedirs('sorted')
 
    # copy files
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            try:
                src_file = os.path.join(root, file)
                ds = pydicom.dcmread(src_file)
                dest_dir_name = generate_dest_dir_name(ds)
                out_dir = 'sorted/' + ds.PatientID 
                print(src_file, dest_dir_name)
                dest_dir = os.path.join(out_dir, dest_dir_name)
                dir_names.append(dest_dir_name)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy2(src_file, dest_dir)
                print("copy %s -> %s" % (src_file, dest_dir))
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
        print(args.dirs[0])
        copy_dicom_files(args.dirs[0])
        print("execution time: %.2f second." % (time.time() - start_time))
    except Exception as e:
        print("%s: error: %s" % (__file__, str(e)))
        err = 1
 
    sys.exit(err)
