"""
Insert attribute DeltaMagnitude into Locus-aggregated DB.

Author: Shuo Yang
Email: imsure95@gmail.com
"""

#!/usr/bin/env python3

import pymysql
import pandas as pd
import os, sys
from datetime import datetime
from antares.config import *

path2demo_data = './demo-data'

def update_db( conn, cur ):
    sql_query = """select AlertID from Alert"""
    cur.execute( sql_query )
    rows = cur.fetchall()

    for row in rows:
        alert_id = row[ 0 ]
        # Open file containing light curve data for 'alert_id'.
        try:
            f = open( os.path.join(path2demo_data, 'lightcurve/'+str(alert_id)+'.dat') )
        except IOError:
            print( "No data file exists for light curve of alert {0}".alert_id )
            exit( -1 )

        ## Fields for AttributeValue table.
        container_id = alert_id
        container_type = 'E' # Alert table

        lines = f.readlines()
        fields = lines[ -1 ].rstrip().lstrip().split()
        time1 = float( fields[ 0 ] )
        mag1 = float( fields[ 1 ] )
        fields = lines[ -2 ].rstrip().lstrip().split()
        time2 = float( fields[ 0 ] )
        mag2 = float( fields[ 1 ] )
        #print( 'Alert {0}: {1}, {2}, {3}, {4}'.format(alert_id, time1, mag1, time2, mag2) )
        delta_mag = abs( mag1 - mag2 )

        sql_insert = """insert into AttributeValue(ContainerID,ContainerType,Value,AttrName)
        values({0},"{1}",{2},"DeltaMagnitude")""".format( alert_id, container_type, delta_mag )
        cur.execute( sql_insert )

        print( 'Alert: {0} with DeltaMagnitude={1}'.format(alert_id, delta_mag) )

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
    update_db( conn, cur )
    

if __name__ == '__main__':
    main()
