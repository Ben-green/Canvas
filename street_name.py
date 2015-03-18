#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import re
import csv
import sqlite3

#print sqlite3.sqlite_version

def main( ):
    db = None
    try:
        db = sqlite3.connect( 't/knocksheets.sqlite' )
        cursor = db.cursor( )

        print 'Creating schema'
        with open( 'HE.ddl', 'rt' ) as fileDDL:
            schema = fileDDL.read()
        db.executescript(schema)

        print 'Importing CSV'
        reader = csv.reader( open( 't/HEZ.csv', 'r' ), delimiter=',' )
        for row in reader:
            to_db = [
                unicode(row[0], "utf8"),
                unicode(row[1], "utf8"),
                unicode(row[2], "utf8"),
                unicode(row[3], "utf8"),
                unicode(row[4], "utf8"),
                unicode(row[5], "utf8"),
                unicode(row[6], "utf8"),
                unicode(row[7], "utf8"),
                unicode(row[8], "utf8"),
                unicode(row[9], "utf8"),
                unicode(row[10], "utf8"),
                unicode(row[11], "utf8"),
                unicode(row[12], "utf8"),
                unicode(row[13], "utf8"),
                unicode(row[14], "utf8"),
                unicode(row[15], "utf8"),
                unicode(row[16], "utf8"),
                unicode(row[17], "utf8")
            ]
            cursor.execute( "INSERT INTO HE (polling_district, elector_number, status, title, first_names, initials, surname, suffix, date_attainment, f_franchise, address_1, address_2, address_3, address_4, address_5, address_6, address_7, f_opt_out ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );", to_db )

        print 'Altering TABLE';
        cursor.execute( "ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
            .format( tn='HE', cn='street_name', ct='TEXT' ))

        cursor.execute( 'SELECT rowid,address_1,address_2,address_3,address_4,address_5,address_6,address_7 FROM HE' )
        #print cursor.rowcount
        for row in cursor.fetchall( ):
            #print row
            textStreetName = None
            for i, col in reversed( list( enumerate( row ) ) ):
                if i == 0:
                    if textStreetName is None:
                        textStreetName = 'GROPE CUNT LANE'
                    cursor.execute( "UPDATE HE SET street_name='{street_name}' WHERE rowid={rowid}"\
                            .format( street_name=textStreetName, rowid=col ) )
                    continue
                #print "[",i,"] " , col
                if textStreetName is None:
                    # Try to get street name from this column
                    if col == '':
                        #print " [", i, "] empty"
                        continue
                    if re.match( '[A-Z]*[0-9]* [0-9]*[A-Z]*$', col ):
                        #print " [", i, "] Post Code"
                        continue
                    if re.match( '[A-Z]*$', col ):
                        #print " [", i, "] City"
                        continue
                    match = re.search( '[A-Z]* [A-Z]*$', col )
                    if match:
                        textStreetName = match.group( 0 )
                        #print " [", i, "] Street: '%s'" % textStreetName
                        continue
                    else:
                        print " [", i, "] No match for: '%s'" % col
                        continue

        print 'Committing result'
        db.commit()

    except Exception as e:
        print "Error %s:" % e.args[ 0 ]
        raise e;

    finally:
        if db:
            db.close( )

    return

if __name__ == "__main__":
    main( )
