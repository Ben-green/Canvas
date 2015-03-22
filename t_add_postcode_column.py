#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import unittest
import re

from add_postcode_column import AddPostcodeColumn
from add_postcode_column import rePostcode

class T( unittest.TestCase ):

    def test_append_empty_field_to_date_row( self ):
        apc = AddPostcodeColumn( )
        result = apc.AppendToRow( 'Date Published: 01/12/2014,,,,,,,,,,,,,,,,,' )
        self.assertEqual( 18, result.count( ',' ), 'Expected 18 commas in my CSV' )
        self.assertTrue( result.endswith( ',' ), 'Expected last field to be empty' )

    def test_append_column_name_to_headings_row( self ):
        apc = AddPostcodeColumn( )
        result = apc.AppendToRow( 'PD,ENO,Status,Title,First Names,Initials,Surname,Suffix,Date of Attainment,Franchise Flag,Address 1,Address 2,Address 3,Address 4,Address 5,Address 6,Address 7,Opt Out' )
        self.assertEqual( 18, result.count( ',' ), 'Expected 18 commas in my CSV' )
        self.assertTrue( result.endswith( ',postcode' ), 'Expected to have added the heading "postcode"' )

    def test_append_empty_field_to_N_row( self ):
        apc = AddPostcodeColumn( )
        result = apc.AppendToRow( 'HAB,1374,,,,,N,,,,,,,,,,,' )
        self.assertEqual( 18, result.count( ',' ), 'Expected 18 commas in my CSV' )
        self.assertTrue( result.endswith( ',' ), 'Expected last field to be empty' )

    def test_append_empty_field_to_OTHER_ELECTORS_row( self ):
        apc = AddPostcodeColumn( )
        result = apc.AppendToRow( 'HAF,2091,E,,Xxxxxx,X,Xxxxxx,,,,"OTHER ELECTORS",,,,,,,Z' )
        self.assertEqual( 18, result.count( ',' ), 'Expected 18 commas in my CSV' )
        self.assertTrue( result.endswith( ',' ), 'Expected last field to be empty' )

    def test_append_postcode_to_elector_row( self ):
        apc = AddPostcodeColumn( )
        postcode='LS14 3DT'
        result = apc.AppendToRow( 'HAA,1,E,,Xxxxxxxx,,Xxxxxxxx,,,,"1 ASPEN DRIVE",SCARCROFT,LEEDS,'+postcode+',,,,' )
        self.assertEqual( 18, result.count( ',' ), 'Expected 18 commas in my CSV' )
        self.assertTrue( re.search( rePostcode, result ), 'Expected last field to be a postcode' )
        self.assertTrue( result.endswith( postcode ), 'Expected last field to be same as given postcode' )
        #print result
