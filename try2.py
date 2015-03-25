#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

"""try2.py: Tests the tent module"""

__author__      = "Joe Salmon"
__copyright__   = "Copyright 2015, Planet Earth"

import tent
import sqlite3

filenamedb = 'something.db'

conn = sqlite3.connect(filenamedb)
# This tells python to start typing in the running sqlite3 program.
cur = conn.cursor()


thingy = 'work/councilfull.csv'
tent.importcsvfile (thingy,filenamedb)
