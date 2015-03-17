#!/usr/bin/perl -w
# vim:set ts=4 sw=4 sts=4 et:

use strict;

use Names;

use Text::CSV_PP;

my $csv = Text::CSV_PP->new (
    { binary => 1 }, # should set binary attribute.
    { quote_space => 0 }
) or die "Cannot use CSV_PP: ".Text::CSV_PP->error_diag ();

while( <> ) {
    $csv->parse($_)
        or die "Can't parse(): " . $csv->error_input();

    my @columns = $csv->fields( );

    # Turn every Polling District into a test value
    $columns[ 0 ] =~ s/(..)./$1Z/ ;

    # All elector numbers above 10000
    my $n = int( 10000 + rand( 9000 ) );
    $columns[ 1 ] = $n;

    # Randomise status
    my $iMax = @Names::status;
    my $i = int( rand( scalar @Names::status ) );
    print STDERR "Using i = $i of $iMax (" . $Names::status[ $i ] . ")\n";
    $columns[ 2 ] = $Names::status[ $i ];

    # Randomise title
    $i = int( rand( @Names::title ) );
    $columns[ 3 ] = $Names::title[ $i ];

    # Randomise first_names
    $i = int( rand( @Names::first_names ) );
    $columns[ 4 ] = $Names::first_names[ $i ];

    # Randomise initials
    $i = int( rand( @Names::initials ) );
    $columns[ 5 ] = $Names::initials[ $i ];

    # Randomise surname
    $i = int( rand( @Names::surname ) );
    $columns[ 6 ] = $Names::surname[ $i ];

    # Randomise suffix
    $i = int( rand( @Names::suffix ) );
    $columns[ 7 ] = $Names::suffix[ $i ];

    # Randomise date_attainment
    $i = int( rand( @Names::date_attainment ) );
    $columns[ 8 ] = $Names::date_attainment[ $i ];

    # Randomise f_franchise
    $i = int( rand( @Names::f_franchise ) );
    $columns[ 9 ] = $Names::f_franchise[ $i ];

    # Randomise f_opt_out
    $i = int( rand( @Names::f_opt_out ) );
    $columns[ 17 ] = $Names::f_opt_out[ $i ];

    $csv->combine( @columns );
    print $csv->string, "\n";
}

$csv->eof
    or $csv->error_diag();


