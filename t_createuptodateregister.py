#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import unittest

from createuptodateregister import createuptodateregister

class T( unittest.TestCase ):

    def test_Wards( self ):
        c = createuptodateregister( )
        for i,ward in enumerate( c.Wards( 2 ) ):
           iLast = i
        self.assertEqual( iLast, 1 )

