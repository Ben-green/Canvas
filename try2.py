#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

"""try2.py: Tests the tent module"""

__author__      = "Joe Salmon"
__copyright__   = "Copyright 2015, Planet Earth"

import tent

#conn = sqlite3.connect(filenamedb)
# This tells python to start typing in the running sqlite3 program.
#cur = conn.cursor()

tent.importcsvfile ( 'work/councilfull.csv', 'work/something.db' )
