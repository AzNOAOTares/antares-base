"""
Populate Locus-aggregated DB from the demo data.

Author: Shuo Yang
Email: imsure95@gmail.com
"""

#!/usr/bin/env python3

import pymysql
import pandas as pd
import os, sys
from datetime import datetime
from antares.config import *

path2fake_alerts = './fake-alerts'
debug = True
#debug = False

def populate_db( conn, cur ):
    
    for index in range( 777001, 777004 ):
        # Open file containing light curve data for 'alert_id'.
        try:
            f = open( os.path.join(path2fake_alerts, str(index)+'.dat') )
        except IOError:
            print( "No data file exists for light curve of alert {0}".format(index) )
            exit( -1 )

        ## Fields for AttributeValue table.
        container_id = index
        container_type = 'E' # Alert table

        for line in f.readlines():
            fields = line.rstrip().lstrip().split()
            computed_at = datetime.fromtimestamp( float(fields[0]) )
            magnitude = fields[ 1 ]
            magnitude_err = fields[ 2 ]
            if debug:
                print( 'computed at: {0}, magnitude: {1}, magnitude error: {2}'.
                       format(computed_at, magnitude, magnitude_err) )

            sql_insert = """insert into AttributeValue(ContainerID,ContainerType,ComputedAt,Value,Annotation,Confidence,AttrName)
            values({0},"{1}","{2}",{3},"",1,"Magnitude")""".format( container_id, container_type, computed_at, magnitude )
            try: 
                cur.execute( sql_insert )
            except Exception:
                pass
            sql_insert = """insert into AttributeValue(ContainerID,ContainerType,ComputedAt,Value,Annotation,Confidence,AttrName)
            values({0},"{1}","{2}",{3},"",1,"MagnitudeErr")""".format( container_id, container_type, computed_at, magnitude_err )
            try: 
                cur.execute( sql_insert )
            except Exception:
                pass

        conn.commit()

## The main function.
def main():
    #sys.path.append( './' )

    ## Connect to mysql database.
    conn = pymysql.connect( host='127.0.0.1',
                            user='root',
                            passwd='',
                            db='antares_demo' )
    cur = conn.cursor()
    populate_db( conn, cur )
    

if __name__ == '__main__':
    main()
