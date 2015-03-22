#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import sys
import re

rePostcode = '[A-Z]{1,2}[0-9]{1,2} [0-9]{1,2}[A-Z]{2}'

class AddPostcodeColumn( object ):

    def AppendToRow( self, rowIn ):
        rowOut = rowIn + ','
        # FIXME demeter
        if rowIn.startswith( 'PD' ):
            rowOut += 'postcode'
        if re.match( '[A-Z]{3},', rowIn ):
            if re.match( '.*,"OTHER ELECTORS",', rowIn ):
                pass
            elif re.match( '(.*,){6}N,', rowIn ):
                pass
            else:
                match = re.search( rePostcode, rowIn )
                if( match ):
                    rowOut += match.group( 0 )
        return rowOut

if( __name__ == "__main__" ):
    apc = AddPostcodeColumn( )
    for line in sys.stdin:
        print apc.AppendToRow( line.rstrip( ) )
