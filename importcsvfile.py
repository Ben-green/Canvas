#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

__author__      = "Joe Salmon"
__copyright__   = "Copyright 2015"

from sys import argv
import sqlite3
import csv
import re

# asks what file to import to a db with what file name
def askaboutimport ( ):
    print "What is the name of the CSV file you would like to import?"
    csvtoimport = raw_input (">")
    print "What is the name of the database you want to work in / create?"
    dbtouse = raw_input (">")
    print "Finally what is the name of the table you want to create with imported CSV data?"
    tablename = raw_input (">")
    importcsvfile (csvtoimport,dbtouse,tablename)
    
# imports a given csv into db with a suggested name
def importcsvfile (csvfile,db,naTable):
    makeheadings (csvfile,db, naTable)
    insertdata (csvfile,db, naTable)

# creates the headings
def makeheadings (csvfile,db, naTable):
    global biggestHead
    global headingsforever
    global biggestrow
    global cur
    global conn

    filereader = csv.reader( open(csvfile, 'rt'), delimiter=',')
    c = 0
    biggestHead = 0
    for fdsa in filereader:
        c = c+1
        if c > 9:
            break
        posHead = 0
        for column in fdsa:
            if column == '':
                break
            else:
                posHead = posHead + 1
        if posHead > biggestHead:
            biggestHead = posHead
            biggestrow = c
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    filereader = csv.reader( open(csvfile, 'rt'), delimiter=',') 
    c=0
    for something in filereader:
        headings = something
        strHeaders = "'" + "','".join( headings ) + "'"
        c=c+1
        if c == biggestrow:            
            columns = biggestHead
            cur.execute("drop table if exists %r;" % (naTable) )       
            cur.execute("create table %r(%s);" % (naTable,strHeaders) )
            print "CREATED TABLE %r, with below headings" % (naTable)
            print headings
            headingsforever = headings           

    #do not ommit this line, without it data would be thrown away.            
    conn.commit()

# adds data
def insertdata (csvfile,db, naTable):
    global biggestHead
    global headingsforever
    global biggestrow
    global cur
    global conn
    filereader = csv.reader( open(csvfile, 'rt'), delimiter=',')
    line = 0
    for something in filereader:
        line = line +1
        columns = biggestHead +1
        headingstouse = headingsforever
        if line > biggestrow:
            #This makes the data into strings.
            strHeaders = "'" + "','".join( headingstouse ) + "'"            
            strSomething = "'" + "','".join( something ) + "'"
            sql = "INSERT INTO %r (%s) VALUES( %s );" % ( naTable, strHeaders, strSomething )
            cur.execute(sql)
            conn.commit()
            print something            
    print "FINISHED adding the above to table %r" % (naTable)     
    conn.commit()
    
