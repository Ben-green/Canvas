#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

from __future__ import print_function

"""createuptodateregister.py: Does nothing of any use to anyone."""

__author__      = "Joe Salmon"
__copyright__   = "Copyright 2015, The Green Party UK"

import sys

class createuptodateregister( object ):
    def Wards( self, n ):
        i = 1      # Start with 'ward01'
        while i <= n:
            yield "ward%02d" % ( i )
            i += 1

    # FIXME Make this a static method?
    def CreateUpToDateRegister( self, inDatabase ):
        for ward in self.Wards( 29 ):
            print( "DROP TABLE IF EXISTS %s;" % ( ward ), file=sys.stdout )
        print( "\n.mode csv", file=sys.stdout )
        # Joe's good stuff goes here

if( __name__ == "__main__" ):
    naDatabase = sys.argv[ 1 ]
    createuptodateregister().CreateUpToDateRegister( naDatabase)
    print( "All done", file=sys.stderr )




# Delete this line and everything below it,  start your programming!
# Why not fill in the doc string at the top, first?
