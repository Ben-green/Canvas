#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

__author__      = "Joe Salmon"
__copyright__   = "Copyright (c) 2015, The Green Party UK"

from sys import argv
import sqlite3
import csv
import re
import os
from os.path import basename

# global variables
naFileCSV = ''
naDataBase = ''
naTable = ''
iRowHeadings = 1
listHeadings = []

def importcsvfile ( csvfile, db ):    #import a csv file called 'csvfile' into an SQlite database called db.
    global naFileCSV, naDataBase, naTable
    naFileCSV = csvfile
    naDataBase = db
    naTable = os.path.splitext( basename( naFileCSV ) )[0]

    HeadingsFromCSV( )
    print "%r: Found %r COLUMN headings in row %r" % ( naFileCSV, len( listHeadings ), iRowHeadings )
    print listHeadings

    return
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    filereader = csv.reader( open(csvfile, 'rt'), delimiter=',') 
    c=0
    for something in filereader:
        c=c+1
        if c == biggestrow:
            cur.execute("drop table if exists dummytable;" )       
            cur.execute("create table dummytable(datanumber);" )
            columns = biggestHead
            headingsforever = something
            for a in something:
                cur.execute("alter table dummytable add column %r;" % (a))
                if columns == 0:
                    break
                else:
                    
                    columns = columns - 1
                 
            
    print "finished checking first tent lines, assuming no data above Headings"
    print "will assume correct headings are %s" % (headingsforever)

    filereader = csv.reader( open(csvfile, 'rt'), delimiter=',') 
    line = 0
    for something in filereader:
        line = line +1
        columns = biggestHead +1
        headingstouse = headingsforever
        if line > biggestrow:
            print "now I am on line %s and need to add the below into one of %s columns" % (line, columns)
            #This makes the data into strings.
            strHeaders = "'" + "','".join( headingstouse ) + "'"
            print strHeaders
            strSomething = "'" + "','".join( something ) + "'"
            sql = "INSERT INTO dummytable (%s) VALUES( %s )" % ( strHeaders, strSomething )
            print sql
            cur.execute(sql)
                
        else:
                print "not adding this line"
                
                 
                
                
    #do not ommit this line, without it data would be thrown away.            
    conn.commit()

def HeadingsFromCSV( ):
    global naFileCSV, iRowHeadings, listHeadings

    # rb : means read, with binary mode ( see https://docs.python.org/2/library/csv.html#module-contents )
    # delimiter : ',' tells the reader to separate fields with commas
    with open( naFileCSV, 'rb' ) as f:
        filereader = csv.reader( f, delimiter=',' )

    # count of lines read, we will stop at 10
    cRow = 0

    # Note how many filled COLUMNs in the most filled-in ROW
    cbestFilledFields = 0

    for fdsa in filereader:
        cRow = cRow+1
        if cRow > 9:
            break

        # Note how many filled COLUMNs in ROW cRow
        cFilledFields = 0
        for column in fdsa:
            if column == '':
                break
            else:
                cFilledFields = cFilledFields + 1

        # If the ROW is more filled in than the current best, then record it
        if  cFilledFields > cbestFilledFields:
            cbestFilledFields = cFilledFields
            iRow = cRow
            rowHeadings = fdsa

    iRowHeadings = iRow
    listHeadings = rowHeadings
