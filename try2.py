#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

__author__      = "Joe Salmon"
__copyright__   = "Copyright (c) 2015-2016, The Green Party UK"

import sqlite3
import importcsvfile
from sys import argv

# This has a go at using specified csv files as existing up to date council data, and another as the existing canvassing records, to 
# create a new file which is up to date. If you want to change the existing data it uses, this must be done by changing the script. It 
# will ask what you want the database file you are using to be called

print """This has a go at using specified csv files as existing uptodate council data, and another as the existing canvassing records, to create a new file which is up to date. If you want to change the existing data it uses, this must be done by changing the script."""

# List of the different files of council data to be used, change this list to change the data that is used, as instructed in STEP 2.
listcouncildata = [
        "councilbig.csv",
        "councildata.csv"
        ]

# Name of the .db file used to store this new data, change this if you want as instructed in STEP 2.
databaseused = "canvas2016.db"

# Name of the .csv file that contains existing data, change this if you want as instructed in STEP 2.
existingcanvas = "old.csv"

print listcouncildata

for fdsa in listcouncildata:
    print "importing council data %s" % (fdsa)
    importcsvfile.importcsvfile (fdsa,databaseused)

print "creating councilfullupdated file" 
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
  "subroad" TEXT,
  "road" TEXT,
  "v12" TEXT,
  "v14" TEXT,
  "v15" TEXT,
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



for bit in listcouncildata:
    print "adding data to councilfull from %s" % (bit)
    with sqlite3.connect( databaseused ) as conn:
        cursor = conn.cursor()
        tobedone = '''insert into councilfullupdated (pd,eno,firstname,surname,fulladdress,address_1,address_2,address_3,address_4,address_5,address_6,address_7,subroad,road,remove) select pd,eno,firstname,surname,address1||address2||address3||address4||address5||address6||address7,address1,address2,address3,address4,address5,address6,address7,subroad,road,remove from %r where remove is not 'D';''' % (bit)
        cursor.execute( tobedone )
        conn.commit()


# creating table of people who need to be removed in the updates

print "creating table of people who need to be removed in the updates" 
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
  "subroad" TEXT,
  "road" TEXT,
  "remove" text
);'''
    cursor.execute( tobedone )
    conn.commit()


# adding to the toremove table

print "adding to the toremove table"


for bit in listcouncildata:
    print "adding data to the toremovetable from %s" % (bit)
    tobedone = '''insert into toremove (pd, eno, firstname, surname, address_1, address_2, address_3, address_4, address_5, address_6, address_7, subroad,road) select pd, eno, firstname, surname, address1, address2, address3, address4, address5, address6, address7, subroad,road
from %r where remove is 'D';''' % (bit)
    cursor.execute( tobedone )
    conn.commit()

 
# setting remove column to remove
print "setting remove column to remove"

with sqlite3.connect( databaseused ) as conn:
    cursor = conn.cursor()
    tobedone = ''' UPDATE toremove SET remove = 'remove';'''
    cursor.execute( tobedone )
    conn.commit()

# creating table councilremovedupdated which now has the remove column populated with remove if someone should be removed

print "creating table councilremovedupdated which now has the remove column populated with remove if someone should be removed"
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
  "subroad" TEXT,
  "road" TEXT,
  "v12" TEXT,
  "v14" TEXT,
  "v15" TEXT,
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
    tobedone = '''insert into councilremovedupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7,subroad,road,remove) 
select 
councilfullupdated.pd, councilfullupdated.eno, councilfullupdated.firstname, councilfullupdated.surname, councilfullupdated.fulladdress, councilfullupdated.street, councilfullupdated.address_1, councilfullupdated.address_2, councilfullupdated.address_3, councilfullupdated.address_4, councilfullupdated.address_5, councilfullupdated.address_6, councilfullupdated.address_7, councilfullupdated.subroad,councilfullupdated.road, toremove.remove from councilfullupdated left outer join toremove on councilfullupdated.firstname = toremove.firstname and councilfullupdated.surname = toremove.surname and councilfullupdated.address_1 = toremove.address_1;'''
    cursor.execute( tobedone )
    conn.commit()

# Creating final table which only contains people who should not be removed from the data
print "Creating final table which only contains people who should not be removed from the data"
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
  "subroad" TEXT,
  "road" TEXT,
  "v12" TEXT,
  "v14" TEXT,
  "v15" TEXT,
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

# added data
print "adding the final bit of data to councilupdated"

with sqlite3.connect( databaseused ) as conn:
    cursor = conn.cursor()
    tobedone = '''insert into councilupdated (pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7,subroad,road) 
select pd, eno, firstname, surname, fulladdress, street, address_1, address_2, address_3, address_4, address_5, address_6, address_7,subroad,road from councilremovedupdated where remove is not 'remove';'''
    cursor.execute( tobedone )
    conn.commit()

# removing duplicate information from council updated
print "removing duplicate information from council updated"

with sqlite3.connect( databaseused ) as conn:
    cursor = conn.cursor()
    tobedone = '''delete from councilupdated where rowid not in 
(select min(rowid) from councilupdated group by firstname, surname, address_1);'''
    cursor.execute( tobedone )
    conn.commit()

# At this point in the old SQL script, the street name field would now be added in. This feature is a little redundant now 
# as we need to work off postcodes, and something to be fixed

print "At this point in the old SQL script, the street name field would now be added in. This feature is a little redundant now as we need to work off postcodes, and something to be fixed"

# We now have a table within the database called councilupdated, which is the current electoral register with all updates taken into account
print "We now have a table within the database called councilupdated, which is the current electoral register with all updates taken into account"


# This part of the script creates a new table for existing canvassing data

print "Creating final table of existing canvassing data"
with sqlite3.connect( databaseused ) as conn:
    cursor = conn.cursor()
    tobedone = 'DROP TABLE if exists freshdata1;'
    cursor.execute( tobedone )
    tobedone = '''CREATE TABLE freshdata1(  
"pd" TEXT,
  "eno" TEXT,
  "firstname" TEXT,
  "surname" TEXT,
  "fulladdress" TEXT,
  "street" TEXT,
  "address1" TEXT,
  "address2" TEXT,
  "address3" TEXT,
  "address4" TEXT,
  "address5" TEXT,
  "address6" TEXT,
  "address7" TEXT,
  "subroad" TEXT,
  "road" TEXT,
  "priorres" TEXT,
  "v12" TEXT,
  "v14" TEXT,
  "v15" TEXT,
  "green" TEXT,
  "intent" TEXT,
  "surveyn" TEXT,
  "yearmovedin" TEXT,
  "knocked" TEXT,
  "other1" TEXT,
  "other2" TEXT,
  "partymember" TEXT
);'''
    cursor.execute( tobedone )
    conn.commit()

importcsvfile.importcsvfile (existingcanvas,databaseused)

listoldcommands = [ 
"alter table '%s' add column v12;" % (existingcanvas), 
"alter table '%s' add column v14;" % (existingcanvas),
"alter table '%s' add column green;" % (existingcanvas),
"alter table '%s' add column intent;" % (existingcanvas),
"alter table '%s' add column surveyn;" % (existingcanvas),
"alter table '%s' add column knocked;" % (existingcanvas),
"alter table '%s' add column other1;" % (existingcanvas),
"alter table '%s' add column other2;" % (existingcanvas),
"alter table '%s' add column yearmovedin;" % (existingcanvas),
"alter table '%s' add column priorres;" % (existingcanvas),
"alter table '%s' add column partymember;" % (existingcanvas),
"update '%s' set priorres = 'yes';" % (existingcanvas) 
        ]

# This should add new columns if needed and update the person as a # prior resident. Currently not working as issue 37

#for bit in listoldcommands:
#    with sqlite3.connect( databaseused ) as conn:
#        cursor = conn.cursor()
#        tobedone = '''%s''' % (bit)
#        print tobedone
#        cursor.execute( tobedone )
#        conn.commit()

# the below is included to update the priorress to yes as it is
# not done above.

with sqlite3.connect( databaseused ) as conn:
    cursor = conn.cursor()
    tobedone = '''update '%s' set priorres = 'yes';''' % (existingcanvas)
    cursor.execute( tobedone )
    conn.commit()

# This merges the council and existing data together into the
# table freshdata1

print "merging data into freshdata1"

with sqlite3.connect( databaseused ) as conn:
    cursor = conn.cursor()
    tobedone = '''
insert into freshdata1 (pd,eno,firstname,surname,fulladdress,street,address1,address2,address3,address4,address5,address6,address7,subroad,road,v12,v14,v15,green,intent,other1,other2,yearmovedin,priorres) 
select councilupdated.pd, councilupdated.eno, councilupdated.firstname, councilupdated.surname, councilupdated.fulladdress, '%s'.street, councilupdated.address_1, councilupdated.address_2,councilupdated.address_3,councilupdated.address_4,councilupdated.address_5,councilupdated.address_6,councilupdated.address_7,councilupdated.subroad,councilupdated.road,
'%s'.v12, '%s'.v14, '%s'.v15, '%s'.green, '%s'.intent, '%s'.other1, '%s'.other2, '%s'.yearmovedin, '%s'.priorres 
from councilupdated 
left outer join '%s' on councilupdated.firstname = '%s'.firstname and councilupdated.surname = '%s'.surname and councilupdated.address_1 = '%s'.address1 
or councilupdated.firstname = '%s'.firstname and councilupdated.surname = '%s'.surname and UPPER(councilupdated.road) = UPPER('%s'.street)
or councilupdated.firstname = '%s'.firstname and councilupdated.surname = '%s'.surname and UPPER(councilupdated.subroad) = UPPER('%s'.address3)
or councilupdated.firstname = '%s'.firstname and councilupdated.surname = '%s'.surname and UPPER(councilupdated.subroad) = UPPER('%s'.address4)
or councilupdated.firstname = '%s'.firstname and councilupdated.surname = '%s'.surname and UPPER(councilupdated.subroad) = UPPER('%s'.address5)
or councilupdated.firstname = '%s'.firstname and councilupdated.surname = '%s'.surname and UPPER(councilupdated.subroad) = UPPER('%s'.address6);
    ''' % (existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas, existingcanvas)
    print tobedone
    print "starting work (this can take a while, make a cup of tea or something.)"
    cursor.execute( tobedone )
    print "done the hard bit"
    conn.commit()
    


# These lines set the year moved in as 2016 for new arrivals to 
# the ward, and set the priorres status to 'no'.

print "adding year of arrival as 2016 and setting priorres to 'no' for new arrivals"
with sqlite3.connect( databaseused ) as conn:
    cursor = conn.cursor()
    tobedone = """update freshdata1 set yearmovedin = '2016' where priorres is not 'yes';"""
    cursor.execute( tobedone )
    tobedone = """update freshdata1 set priorres = 'no' where yearmovedin is '2016';"""
    cursor.execute( tobedone )
    tobedone = """delete from freshdata1 where rowid not in 
(select min(rowid) from freshdata1 group by firstname, surname, address1);"""
    cursor.execute( tobedone )
    conn.commit()








