#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import unittest
import glob
import re
import sqlite3
from councilupdate import CouncilUpdate


# If the same database file is used, fails don't always show when testing the findcouncildata bit of the file

naDataBase = 'testme.db'


class T( unittest.TestCase ):



# This first test doesn't work
    def test_createcouncilupdatefiles (self):
        cu = CouncilUpdate ( )
        cu.createcouncilupdatefiles ( naDataBase )
        with sqlite3.connect( naDataBase ) as conn:
            cursor = conn.cursor()
            tobedone = '''PRAGMA table_info(councilfullupdated)'''
            cursor.execute( tobedone )
            r = cursor.fetchall ( )
            table1 = r[ 5 ]
            print table1
            self.assertEqual('notsurehowtest', table1, 'table isnt right or test (It is the test, it would probably work if this had been written in Gvim' )

# I cannot think how to test this part of the Councilupdate.py file
    def test_findcouncildata (self):
        cu = CouncilUpdate ( )
        cu.createcouncilupdatefiles ( naDataBase )
        cu.findcouncildata ( naDataBase )
        for files in glob.glob("*.csv"):
            with sqlite3.connect( naDataBase ) as conn:
                cursor = conn.cursor()
                tobedone = '''select * from %r;''' % (files)
                cursor.execute( tobedone )
                r = cursor.fetchone ( )
                checkingfile = r[ 0 ]
                print checkingfile
        print checkingfile
        self.assertIsNotNone(checkingfile, 'nothing in the file')


    def test_addingtocouncilupdated ( self ):
        cu = CouncilUpdate ( )
        cu.createcouncilupdatefiles ( naDataBase )
        with sqlite3.connect( naDataBase ) as conn:
            cursor = conn.cursor()
            tobedone = '''insert into councilremovedupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7, remove) VALUES ("HEA","54","Joe","Salmon","24 ASH CRESCENTLEEDSLS6 3LE","","24 ASH CRESCENT","LEEDS","LS6 3LE","","","","","")'''
            cursor.execute( tobedone )
            tobedone = '''insert into councilremovedupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7, remove) VALUES ("HEA","33","James","Armstong","23 ASH CRESCENTLEEDSLS6 3LE","","24 ASH CRESCENT","LEEDS","LS6 3LE","","","","","remove")'''
            cursor.execute( tobedone )
            tobedone = '''insert into councilremovedupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7, remove) VALUES ("HEA","33","Ben","Fowler","27 ASH CRESCENTLEEDSLS6 3LE","","24 ASH CRESCENT","LEEDS","LS6 3LE","","","","","")'''
            cursor.execute( tobedone )
            tobedone = '''insert into councilremovedupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7, remove) VALUES ("HEA","33","Ben","Fowler","27 ASH CRESCENTLEEDSLS6 3LE","","24 ASH CRESCENT","LEEDS","LS6 3LE","","","","","")'''
            cursor.execute( tobedone )
            conn.commit()
            tobedone = '''select COUNT( * ) from councilremovedupdated'''
            cursor.execute( tobedone )
            row = cursor.fetchone ( )
            cBefore = row[ 0 ]
            print "printing cBefore %r" % (cBefore)
            cu.addingtocouncilupdated (naDataBase)
            tobedone = '''select COUNT( * ) from councilupdated'''
            cursor.execute( tobedone )
            row = cursor.fetchone ( )
            cAfter = row[ 0 ]
            print "printing cAfter %r" % (cAfter)
            self.assertEqual( 4, cBefore, 'Provided 4 ROWs with one duplicate, and one to remove' )
            self.assertEqual( 2, cAfter, 'Leaving 2 ROWs' )

    def test_addingpostcodes ( self ):
        cu = CouncilUpdate ( )
        cu.createcouncilupdatefiles ( naDataBase )
        with sqlite3.connect( naDataBase ) as conn:
            cursor = conn.cursor()
            tobedone = '''insert into councilupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7) VALUES ("HEA","310","Phil","Daley","16 DERWENTWATER GROVELEEDSLS6 3EN","","16 DERWENTWATER GROVE","LEEDS","LS6 3EN","","","","")
'''
            cursor.execute( tobedone )
            tobedone = '''insert into councilupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7) VALUES ("HEA","310","Julie","Fillery","53 DERWENTWATER GROVELEEDSLS3 8RE","","16 DERWENTWATER GROVE","LEEDS","LS3 8RE","","","","")
'''
            cursor.execute( tobedone )
            conn.commit()
            cu.addingpostcodes (naDataBase)
            tobedone = '''select postcode from councilupdated'''
            cursor.execute( tobedone )
            row = cursor.fetchone ( )
            cPostcode = row[ 0 ]
            print "printing cPostcode %r" % (cPostcode)
            self.assertEqual('LS6 3EN', cPostcode, 'Postcode isnt correct')
        


#        self.assertEqual( 18, result.count( ',' ), 'Expected 18 commas in my CSV' )
#        self.assertTrue( result.endswith( ',' ), 'Expected last field to be empty' )


#def addingtocouncilupdated (databaseused):
#   # added data
#  print "adding the final bit of data to councilupdated"
# with sqlite3.connect( databaseused ) as conn:
    #   cursor = conn.cursor()
     #  tobedone = '''insert into councilupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7) 
#select pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7 from #councilremovedupdated where remove is not 'remove';'''
#       cursor.execute( tobedone )
#       conn.commit()
    # removing duplicate information from council updated
 #      print "removing duplicate information from council updated"
  #     tobedone = '''delete from councilupdated where rowid not in 
# (select min(rowid) from councilupdated group by firstname, surname, address_1);'''
   #    cursor.execute( tobedone )
    #   conn.commit()
