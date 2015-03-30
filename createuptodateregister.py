#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:
"""createuptodateregister.py: Does nothing of any use to anyone, yet."""
__author__ = "Joe Salmon"
__copyright__ = "Copyright 2015, The Green Party UK"

import importcsvfile
import sqlite3, csv
from sys import argv
        
def csvregs(n):
    i = 0
    while i < n:
        yield "rawfile%02d" % ( i ) 
        i += 1

# creates a number of tables called the rawfile** from given CSVs in a specified table*
def startofp ( ):
    global numbercsvreg
    global nadb
    print "How many csv files contain electoral register information you need to use?"
    numbercsvreg = input(">")
    if numbercsvreg >= 100:
        print "this isn't going to work, use less files"
    else:
        print """wonderful, so you need %r files to be turned into some CSVs. Later on this will also give 
        you the option to add in canvassing returns and have the members database taken into account.""" % (numbercsvreg)
        print "what is the name of the db you want to work on?"
        nadb = raw_input(">")
        for something in csvregs(numbercsvreg):
            print "importing csv as %s what is the csv called?" % (something)
            csvtoimport = raw_input(">")
            importcsvfile.importcsvfile(csvtoimport, nadb, something)        

## adds the already created rawfiles into one big table called alldata
def middleofp ( ):
    global numbercsvreg
    global nadb
    conn = sqlite3.connect(nadb)
    cur = conn.cursor()
    cur.execute ("""DROP TABLE if exists alldata;""")
    cur.execute ("""CREATE TABLE alldata("pd" TEXT,  "eno" TEXT,  "stat" TEXT,  "title" TEXT,  "firstname" TEXT,  
        "initials" TEXT,  "surname" TEXT,
        "suffix" TEXT,  "dateofattainment" TEXT,  "franchiseflag" TEXT,  "address1" TEXT,  "address2" TEXT,  "address3" TEXT,
        "address4" TEXT, "address5" TEXT,  "address6" TEXT,  "address7" TEXT,  "optout" TEXT,  "postcode" TEXT);""")
    print "combining %s raw files, are all required Headings the same? y/n" % (numbercsvreg)
    yesno = raw_input (">")
    if yesno == "n":
        for something in csvregs(numbercsvreg):
            print "in the files what is the name of the PD colmn?" 
            pdcol = raw_input (">")
            print "in the files what is the name of the ENO colmn?"
            enocol = raw_input (">")
            print "in the files what is the name of the Status colmn?"
            statuscol = raw_input (">")
            print "in the files what is the name of the Firstname colmn?"
            firstnacol = raw_input (">")
            print "in the files what is the name of the Surname colmn?"
            surnacol = raw_input (">")
            print "in the files what is the name of the 1th Address colmn?"
            add1col = raw_input (">")
            print "in the files what is the name of the 2th Address colmn?"
            add2col = raw_input (">")
            print "in the files what is the name of the 3th Address colmn?"
            add3col = raw_input (">")           
            print "in the files what is the name of the 4th Address colmn?"
            add4col = raw_input (">")            
            print "in the files what is the name of the 5th Address colmn?"
            add5col = raw_input (">")
            print "in the files what is the name of the 6th Address colmn?"
            add6col = raw_input (">")
            print "in the files what is the name of the 7th Address colmn?"
            add7col = raw_input (">")
            sql = """INSERT INTO alldata (pd, eno, stat, firstname, surname, address1, address2, address3, address4, address5, address6, address7) select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s from %s ;""" % (pdcol, enocol, statuscol, firstnacol, surnacol, add1col, add2col, add3col, add4col, add5col, add6col, add7col, something)
            print sql
            cur.execute (sql) 
            conn.commit ()
    else:
        print "assuming all names same"
        print "are column names unchanged default? y/n"
        answer = raw_input (">")
        if answer == "n":
            print "in the files what is the name of the PD colmn?" 
            pdcol = raw_input (">")
            print "in the files what is the name of the ENO colmn?"
            enocol = raw_input (">")
            print "in the files what is the name of the Status colmn?"
            statuscol = raw_input (">")
            print "in the files what is the name of the Firstname colmn?"
            firstnacol = raw_input (">")
            print "in the files what is the name of the Surname colmn?"
            surnacol = raw_input (">")
            print "in the files what is the name of the 1th Address colmn?"
            add1col = raw_input (">")
            print "in the files what is the name of the 2th Address colmn?"
            add2col = raw_input (">")
            print "in the files what is the name of the 3th Address colmn?"
            add3col = raw_input (">")           
            print "in the files what is the name of the 4th Address colmn?"
            add4col = raw_input (">")            
            print "in the files what is the name of the 5th Address colmn?"
            add5col = raw_input (">")
            print "in the files what is the name of the 6th Address colmn?"
            add6col = raw_input (">")
            print "in the files what is the name of the 7th Address colmn?"
            add7col = raw_input (">")
            for something in csvregs(numbercsvreg):
                sql = """INSERT INTO alldata (pd, eno, stat, firstname, surname, address1, address2, address3, address4, address5, address6, address7) select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s from %s ;""" % (pdcol, enocol, statuscol, firstnacol, surnacol, add1col, add2col, add3col, add4col, add5col, add6col, add7col, something)
                print sql
                cur.execute (sql) 
                conn.commit ()
        else:
            print "assuming all column names unchanged default"
            pdcol = "PD"
            enocol = "ENO"
            statuscol = "[Status]"
            firstnacol = "[First Name]"
            surnacol = "Surname"
            add1col = "[Address 1]"
            add2col = "[Address 2]"
            add3col = "[Address 3]"
            add4col = "[Address 4]"
            add5col = "[Address 5]"
            add6col = "[Address 6]"
            add7col = "[Address 7]"
            for something in csvregs(numbercsvreg):
                sql = """INSERT INTO alldata (pd, eno, stat, firstname, surname, address1, address2, address3, address4, address5, address6, address7) select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s from %s ;""" % (pdcol, enocol, statuscol, firstnacol, surnacol, add1col, add2col, add3col, add4col, add5col, add6col, add7col, something)
                print sql
                cur.execute (sql) 
                conn.commit ()

def returnmiddlepstart ( ):
    middleofp ()

print "lets go, this won't work with over 100 files"
startofp ( )
middleofp ()
    
    
