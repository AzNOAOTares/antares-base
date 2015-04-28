"""
Global helper functions.
"""

#!/usr/bin/env python3

from antares.alert import *
from antares.context import *
from antares.config import *
import os
import pandas as pd
import pymysql

def GenerateCameraAlertStream( alert_num=10 ):
    """
    Randomly generate a stream of camera alerts from the demo database.
    """
    ## Connect to mysql database.
    conn = pymysql.connect( host='127.0.0.1',
                            user='root',
                            passwd='',
                            db='antares_demo' )
    cur = conn.cursor()
    
    alerts = [] # list of camera alerts to be returned to caller.
    for index in range( 0, alert_num ):
        ca_context = CAContext()

        query = """select * from Alert where LocusID={0}""".format(index)
        cur.execute( query )
        alert_row = cur.fetchall()[ 0 ]
        query = """select * from Locus where LocusID={0}""".format(index)
        cur.execute( query )
        locus_row = cur.fetchall()[ 0 ]

        alert_id = alert_row[ 0 ]
        ra = locus_row[ 1 ]
        decl = locus_row[ 2 ]

        ca_context.RA.value = ra
        ca_context.Decl.value = decl

        query = """select Value from AttributeValue where ContainerID={0} and
        ContainerType="E" and AttrName="Magnitude" """.format( alert_id )
        cur.execute( query )
        mag_rows = cur.fetchall()
        # The most-recenctly computed magnitude value.
        magnitude = mag_rows[len(mag_rows)-1][0]

        query = """select Value from AttributeValue where ContainerID={0} and
        ContainerType="E" and AttrName="MagnitudeErr" """.format( alert_id )
        cur.execute( query )
        magerr_rows = cur.fetchall()
        # The most-recenctly computed magnitude value.
        magnitude_err = magerr_rows[len(magerr_rows)-1][0]

        ca_context.Magnitude.value = magnitude
        ca_context.MagnitudeErr.value = magnitude_err
        #print( alert_id, ra, decl, magnitude, magnitude_err )
        #print( type(magnitude) )

        alert = CameraAlert( alert_id, ra, decl, ca_context )
        alerts.append( alert )

    return alerts # return the generated camera alert stream
