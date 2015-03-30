#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

"""createuptodateregister.py: Does nothing of any use to anyone."""

__author__      = "Joe Salmon"
__copyright__   = "Copyright 2015, The Green Party UK"

import importcsvfile
import sqlite3, csv
from sys import argv
        
def csvregs(n):
    i = 0
    while i < n:
        yield "rawfile%02d" % ( i ) 
        i += 1


naDatabase = sys.argv[ 1 ]
CreateUpToDateRegister( naDatabase)
print "All done"




# Delete this line and everything below it,  start your programming!
# Why not fill in the doc string at the top, first?
