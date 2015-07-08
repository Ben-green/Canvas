#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

__author__      = "Joe Salmon"
__copyright__   = "Copyright (c) 2015, The Green Party UK"

import glob
import sqlite3
import importcsvfile
import addpostcode
import sys
import re
from sys import argv


# This program creates a new table within a specified database containing updated information from the electoral register, using a text file which gives the names of the files used by the electoral register.
class CouncilUpdate:

    # This def creates the required tables
    def createcouncilupdatefiles (self, databaseused):
        print "creating required tables" 
        with sqlite3.connect( databaseused ) as conn:
            cursor = conn.cursor()
            tobedone = 'DROP TABLE if exists councilfullupdated;'
            cursor.execute( tobedone )
            conn.commit()
            tobedone = '''CREATE TABLE councilfullupdated(
      "pd" TEXT,
      "eno" TEXT,
      "firstname" TEXT,
      "surname" TEXT,
      "fulladdress" TEXT,
      "street" TEXT,
      "address_1" TEXT,
          "address_2" TEXT,
      "address_3" TEXT,
      "address_4" TEXT,
      "address_5" TEXT,
      "address_6" TEXT,
      "address_7" TEXT,
      "v12" TEXT,
      "v14" TEXT,
      "green" TEXT,
      "intent" TEXT,
      "surveyn" TEXT,
      "knocked" TEXT
      "other1" TEXT,
      "other2" TEXT,
      "remove"
    );'''
            cursor.execute( tobedone )
            conn.commit()
             
            with sqlite3.connect( databaseused ) as conn:
                cursor = conn.cursor()
                tobedone = 'DROP TABLE if exists toremove;'
                cursor.execute( tobedone )
                tobedone = '''CREATE TABLE toremove(
      "pd" TEXT,
      "eno" TEXT,
      "firstname" TEXT,
      "surname" TEXT,
      "fulladdress" TEXT,
      "street" TEXT,
      "address_1" TEXT,
      "address_2" TEXT,
      "address_3" TEXT,
      "address_4" TEXT,
      "address_5" TEXT,
      "address_6" TEXT,
      "address_7" TEXT,
      "remove" text
    );'''
                cursor.execute( tobedone )
                conn.commit()

                with sqlite3.connect( databaseused ) as conn:
                    cursor = conn.cursor()
                    tobedone = 'DROP TABLE if exists councilremovedupdated;'
                    cursor.execute( tobedone )
                    tobedone = '''CREATE TABLE councilremovedupdated(
      "pd" TEXT,
      "eno" TEXT,
      "firstname" TEXT,
      "surname" TEXT,
      "fulladdress" TEXT,
      "street" TEXT,
      "address_1" TEXT,
      "address_2" TEXT,
      "address_3" TEXT,
      "address_4" TEXT,
      "address_5" TEXT,
      "address_6" TEXT,
      "address_7" TEXT,
      "v12" TEXT,
      "v14" TEXT,
      "green" TEXT,
      "intent" TEXT,
      "surveyn" TEXT,
      "knocked" TEXT
      "other1" TEXT,
      "other2" TEXT,
      "remove")
    '''
                    cursor.execute( tobedone )
                    conn.commit()
                    
                    with sqlite3.connect( databaseused ) as conn:
                        cursor = conn.cursor()
                        tobedone = 'DROP TABLE if exists councilupdated;'
                        cursor.execute( tobedone )
                        tobedone = '''CREATE TABLE councilupdated(  
      "pd" TEXT,
      "eno" TEXT,
      "firstname" TEXT,
      "surname" TEXT,
      "fulladdress" TEXT,
      "street" TEXT,
      "address_1" TEXT,
      "address_2" TEXT,
      "address_3" TEXT,
      "address_4" TEXT,
      "address_5" TEXT,
      "address_6" TEXT,
      "address_7" TEXT,
      "v12" TEXT,
      "v14" TEXT,
      "green" TEXT,
      "intent" TEXT,
      "surveyn" TEXT,
      "knocked" TEXT
      "other1" TEXT,
      "other2" TEXT,
      "remove");
    '''
                        cursor.execute( tobedone )
                        conn.commit()
                        print "done!"


        
    def findcouncildata (self, databaseused):
        for files in glob.glob("*.csv"):
            importcsvfile.importcsvfile (files,databaseused)
            
    # This def adds data to the councilful table 
    def addcouncilfull (self, databaseused):
        for files in glob.glob("*.csv"):
            print "adding data to councilfull from %s" % (files)
            with sqlite3.connect( databaseused ) as conn:
                cursor = conn.cursor()
                tobedone = '''insert into councilfullupdated (pd,eno,firstname,surname,fulladdress,address_1,address_2,address_3,address_4,address_5,address_6,address_7, remove) select pd,eno,firstname,surname,address1||address2||address3||address4||address5||address6||address7,address1,address2,address3,address4,address5,address6,address7, remove from %r where remove is not 'D';''' % (files)
                cursor.execute( tobedone )
                conn.commit()

    def addtoremove (self, databaseused):
    # creating table of people who need to be removed in the updates
    # adding to the toremove table
        for files in glob.glob("*.csv"):
            with sqlite3.connect( databaseused ) as conn:
               cursor = conn.cursor()
               print "adding data to the toremovetable from %s" % (files)
               tobedone = '''insert into toremove (pd, eno, firstname, surname, address_1, address_2, address_3, address_4, address_5, address_6, address_7) select pd, eno, firstname, surname, address1, address2, address3, address4, address5, address6, address7
    from %r where remove is 'D';''' % (files)
               cursor.execute( tobedone )
               conn.commit()
                        #setting remove to remove
        print "setting remove to remove"
        tobedone = ''' UPDATE toremove SET remove = 'remove';'''
        cursor.execute( tobedone )
        conn.commit()
        
    def addingcouncilremoved (self, databaseused):
        print "adding to table councilremovedupdated which now has the remove column populated with remove if someone should be removed"
        #adding to table councilremovedupdated which now has the remove column populated with remove if someone should be removed
        with sqlite3.connect( databaseused ) as conn:
           cursor = conn.cursor()
           tobedone = '''insert into councilremovedupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7, remove) 
    select 
    councilfullupdated.pd, councilfullupdated.eno, councilfullupdated.firstname, councilfullupdated.surname, councilfullupdated.fulladdress, councilfullupdated.street, councilfullupdated.address_1, councilfullupdated.address_2, councilfullupdated.address_3, councilfullupdated.address_4, councilfullupdated.address_5, councilfullupdated.address_6, councilfullupdated.address_7, toremove.remove from councilfullupdated left outer join toremove on councilfullupdated.firstname = toremove.firstname and councilfullupdated.surname = toremove.surname and councilfullupdated.address_1 = toremove.address_1;'''
           cursor.execute( tobedone )
           conn.commit()

    def addingtocouncilupdated (self, databaseused):
        # added data
        print "adding the final bit of data to councilupdated"
        with sqlite3.connect( databaseused ) as conn:
           cursor = conn.cursor()
           tobedone = '''insert into councilupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7) 
    select pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7 from councilremovedupdated where remove is not 'remove';'''
           cursor.execute( tobedone )
           conn.commit()
        # removing duplicate information from council updated
           print "removing duplicate information from council updated"
           tobedone = '''delete from councilupdated where rowid not in 
    (select min(rowid) from councilupdated group by firstname, surname, address_1);'''
           cursor.execute( tobedone )
           conn.commit()
           
    def addingpostcodes (self, databaseused):
        print "adding postcode column"
        with sqlite3.connect( databaseused ) as conn:
           cursor = conn.cursor()
           tobedone = '''alter table councilupdated add column postcode;'''
           cursor.execute( tobedone )
           tobedone = '''select * from councilupdated;'''
           for row in cursor.execute( tobedone ):
            print row
            for a in row:
                looking = a
                if re.match('[A-Z]{1,2}[0-9]{1,2} [0-9]{1,2}[A-Z]{2}', looking):
                    print "FOUND A POSTCODE!"
                    print a
                    print "FOUND A POSTCODE!"
                    pass
                else:
                    pass
                
           
#        rePostcode = '[A-Z]{1,2}[0-9]{1,2} [0-9]{1,2}[A-Z]{2}'
#
#class AddPostcodeColumn( object ):
#
#    def AppendToRow( self, rowIn ):
#        rowOut = rowIn + ','
#        # FIXME demeter
#        if rowIn.startswith( 'PD' ):
#            rowOut += 'postcode'
#        if re.match( '[A-Z]{3},', rowIn ):
#            if re.match( '.*,"OTHER ELECTORS",', rowIn ):
#                pass
#            elif re.match( '(.*,){6}N,', rowIn ):
#                pass
#            else:
#                match = re.search( rePostcode, rowIn )
#                if( match ):
#                    rowOut += match.group( 0 )
#        return rowOut
#
#if( __name__ == "__main__" ):
#    apc = AddPostcodeColumn( )
#    for line in sys.stdin:
#        print apc.AppendToRow( line.rstrip( ) )
#        
#        
#        addpostcode.AddPostcodeColumn(  ):

    
