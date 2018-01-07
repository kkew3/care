#!/usr/bin/python3
import sys
import os
cd = os.path.dirname(__file__)

# test if `magic` module works
import magic
testr_dir = os.path.join(os.path.dirname(cd), 'test-resources')
print(magic.from_file(os.path.join(testr_dir, 'libunwind-1.2.tar.gz')))
print(magic.from_file(os.path.join(testr_dir, 'papi_5.4.3.orig.tar.gz')))
print(magic.from_file(os.path.join(testr_dir, 'pdt_lite.tgz')))
print(magic.from_file(os.path.join(testr_dir, 'boxcutter-1.5.zip')))

# # test car functions
# sys.path.append(os.path.dirname(cd))
# import car
