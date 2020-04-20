#!/usr/bin/env python3

"""
Main.
load - Load a program into memory
alu - Arithmetic logic unit
trace - print out CPU state. Call from run() to debug
run - run the CPU
"""

import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()