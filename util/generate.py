#!/usr/bin/env python
# coding: utf-8

import os
import sys

args = sys.argv
args.pop(0) # "generate.py"
name = args.pop(0)
conf_name = args.pop(0)
code_files = args

start = """begin remote 
"""
header = """flags RAW_CODES
eps 30
aeps 100
gap 200000
toggle_bit_mask 0x0

begin raw_codes
"""
end = """end raw_codes
end remote
"""

conf_file = open(conf_name, "w")
conf_file.write(start + "\n")
conf_file.write("name " + name + "\n")
conf_file.write(header + "\n")

for code_file in code_files:
    conf_file.write("name " + os.path.basename(code_file) + "\n")
    cf = open(code_file, "r")
    conf_file.write(cf.read())
    cf.close()
    conf_file.write("\n")

conf_file.write(end)
conf_file.close()
