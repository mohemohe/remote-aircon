#!/usr/bin/env python
# coding: utf-8

import signal
import sys

signal.signal(signal.SIGINT, signal.SIG_IGN)

buff = sys.stdin.read().splitlines()
buff.pop(0)

raw_data = []

for i, line in enumerate(buff):
    elements = line.split()
    raw_data.append(elements[1])
    if (i+1) % 8 == 0:
        raw_data.append("\n")

print(" ".join(raw_data))
