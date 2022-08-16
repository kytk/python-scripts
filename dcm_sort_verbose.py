#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DICOM sorting script using pydicom
# This script is based on the script provided by Yuya Saito

# 29 Dec 2021 K. Nemoto
 
import sys, os, time, re, shutil, argparse, subprocess
import pydicom
 
__version__ = '1.0 (2021/12/29)'
 
__desc__ = '''
sort dicom files.
'''
__epilog__ = '''
examples:
  dcm_sort DICOM_DIR
'''

def generate_dest_dir_name(dicom_dataset):
    name = "%d_%s-%s_%s" % (dicom_dataset.SeriesNumber, dicom_dataset.SeriesDate, dicom_dataset.SeriesTime, dicom_dataset.SeriesDescription)
     
    name = re.sub(r'/', '-', name)
    name = re.sub(r' ', '_', name)
    name = re.sub(r'\*', 'x', name)
    return re.sub(r'[\\|/|:|?|"|<|>|\|]', '', name)

def copy_dicom_files(src_dir):
    dir_names = []
 
    # copy files
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            try:
                src_file = os.path.join(root, file)
                ds = pydicom.dcmread(src_file)
                dest_dir_name = generate_dest_dir_name(ds)
                out_dir = ds.PatientID + '_sorted'
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
#    parser.add_argument('-o', '--out', metavar='OUT_DIR', default='.', help='output directory. default: CWD')
#    parser.add_argument('-n', '--nifdir', metavar='NIFTI_DIR', help='convert nifti to NIFTI_DIR.', default=None)
 
    err = 0
    try:
        args = parser.parse_args()
        print(args.dirs[0])
        #print(args.out)
        #copy_dicom_files(args.dirs[0], args.out)
        copy_dicom_files(args.dirs[0])
        print("execution time: %.2f second." % (time.time() - start_time))
    except Exception as e:
        print("%s: error: %s" % (__file__, str(e)))
        err = 1
 
    sys.exit(err)
