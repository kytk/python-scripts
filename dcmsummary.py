#!/usr/bin/python3

from pydicom import dcmread
import sys

args = sys.argv

ds = dcmread(args[1])

print(ds)


