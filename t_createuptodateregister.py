#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import unittest
import re

from createuptodateregister import createuptodateregister

class T( unittest.TestCase ):

    def test_Wards( self ):
        c = createuptodateregister( )
        for i,ward in enumerate( c.Wards( 2 ) ):
           iLast = i
        self.assertEqual( iLast, 1 )

    def test_ListOfWards( self ):
        c = createuptodateregister( )
        for i,ward in enumerate( c.ListOfWards( ) ):
            self.assertTrue( re.match( '[A-Z][a-zA-Z_]', ward ) )
            iLast = i
        self.assertEqual( iLast, 28 )

    def test_CommandDropTable( self ):
        c = createuptodateregister( )
        strTable = "test"
        str = c.CommandDropTable( strTable )
        self.assertEqual( str, "DROP TABLE IF EXISTS %s;" % ( strTable )  )
