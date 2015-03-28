#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

"""createuptodateregister.py: Does nothing of any use to anyone."""

__author__      = "Joe Salmon"
__copyright__   = "Copyright 2015, The Green Party UK"

import sys

def Wards(n):
    i = 1      # Start with 'ward01'
    while i <= n:
        yield "ward%02d" % ( i )
        i += 1

def CreateUpToDateRegister( inDatabase ):
    for ward in Wards( 29 ):
        print "DROP TABLE IF EXISTS %s;" % ( ward )
    # Joe's good stuff goes here

naDatabase = sys.argv[ 1 ]
CreateUpToDateRegister( naDatabase)
print "All done"




# Delete this line and everything below it,  start your programming!
# Why not fill in the doc string at the top, first?
