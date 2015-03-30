#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

from __future__ import print_function

"""createuptodateregister.py: Does nothing of any use to anyone."""

__author__      = "Joe Salmon"
__copyright__   = "Copyright 2015, The Green Party UK"

import sys

listWards = [
        "Adel_and_Wharfedale",
        "Alwoodley",
        "Ardsley_and_Robin_Hood",
        "Beeston_and_Holbeck",
        "Burmantofts_and_Richmond_Hill",
        "Calverley_and_Farsley",
        "Chapel_Allerton",
        "City_and_Hunslet",
        "Cross_Gates_and_Whinmoor",
        "Garforth_and_Swillington",
        "Gipton_and_Harehills",
        "Guiseley_and_Rawdon",
        "Harewood",
        "Headingley",
        "Horsforth",
        "Hyde_Pary_and_Woodhouse",
        "Killingbeck_and_Secroft",
        "Kippax_and_Methley",
        "Middleton_Park",
        "Moortown",
        "Morley_North",
        "Morley_South",
        "Otley_and_Yeadon",
        "Pudsey",
        "Rothwell",
        "Roundhay",
        "Temple_Newsam",
        "Weetwood",
        "Wetherby"
        ]

class createuptodateregister( object ):
    def ListOfWards( self ):
        for strWard in listWards:
            yield strWard

    def Wards( self, n ):
        i = 1      # Start with 'ward01'
        while i <= n:
            yield "ward%02d" % ( i )
            i += 1

    def CommandDropTable( self, strTable ):
        return "DROP TABLE IF EXISTS %s;" % ( strTable )

    # FIXME Make this a static method?
    def CreateUpToDateRegister( self, inDatabase ):
        for ward in self.Wards( 29 ):
            print( self.CommandDropTable( ward ), file=sys.stdout )
        print( "\n.mode csv", file=sys.stdout )
        for i,strWard in enumerate( self.ListOfWards( ) ):
            print( ".import P141201_%s.csv ward%02d" % ( strWard, i + 1 ), file=sys.stdout )
        # Joe's good stuff goes here

if( __name__ == "__main__" ):
    naDatabase = sys.argv[ 1 ]
    createuptodateregister().CreateUpToDateRegister( naDatabase)
    print( "All done", file=sys.stderr )




# Delete this line and everything below it,  start your programming!
# Why not fill in the doc string at the top, first?
