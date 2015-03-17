#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

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
