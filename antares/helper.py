"""
Global helper functions.
"""

from antares.alert import *
from antares.context import *
from antares.config import *
import os
import pandas as pd
import pymysql

def GenerateFakeAlerts():
    return [ 777001, 777002, 777003 ]

def GenerateCameraAlertStream( alert_num=10 ):
    """
    Generate a stream of camera alert IDs from the demo database.
    """
    ## Connect to mysql database.
    conn = pymysql.connect( host='127.0.0.1',
                            user='root',
                            passwd='',
                            db='antares_demo' )
    cur = conn.cursor()
    
    alert_ids = [] # list of camera alert ids to be returned to caller.

    query = """select AlertID from Alert"""
    cur.execute( query )
    alert_rows = cur.fetchall()
    for row in alert_rows:
        if alert_num == 0:
            break
        
        alert_id = row[ 0 ]
        query = """select Value from AttributeValue where ContainerID={0} \
        and ContainerType='E' and attrname='DeltaMagnitude'""".format(alert_id)
        cur.execute( query )
        delta_mag = cur.fetchall()[0][0]
        if delta_mag > 0.1:
            alert_ids.append( alert_id )
            alert_num -= 1

    conn.close()
    return alert_ids # return the generated camera alert stream

def ConstructCameraAlertFromID( alert_id ):
    ## Connect to mysql database.
    conn = pymysql.connect( host='127.0.0.1',
                            user='root',
                            passwd='',
                            db='antares_demo' )
    cur = conn.cursor()

    ## Fetch alert data
    query = """select * from Alert where AlertID={0}""".format( alert_id )
    cur.execute( query )
    alert_row = cur.fetchall()[ 0 ]
    locus_id = alert_row[ 2 ]
    decision = alert_row[ 1 ]

    ## Fetch Locus data
    query = """select * from Locus where LocusID={0}""".format( locus_id )
    cur.execute( query )
    locus_row = cur.fetchall()[ 0 ]
    ra = locus_row[ 1 ]
    decl = locus_row[ 2 ]

    ca_context = CAContext( alert_id )
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

    query = """select Value from AttributeValue where ContainerID={0} and
    ContainerType="E" and AttrName="DeltaMagnitude" """.format( alert_id )
    cur.execute( query )
    delta_mag_rows = cur.fetchall()
    # The most-recenctly computed magnitude value.
    delta_magnitude = delta_mag_rows[len(delta_mag_rows)-1][0]

    ca_context.Magnitude.value = magnitude
    ca_context.MagnitudeErr.value = magnitude_err
    ca_context.DeltaMagnitude.value = delta_magnitude
    #print( alert_id, ra, decl, magnitude, magnitude_err )
    #print( type(magnitude) )

    alert = CameraAlert( alert_id, ra, decl, ca_context, decision, locus_id )
    
    conn.close()
    return alert # return the generated camera alert

def ConstructAlertReplicaFromID( replica_id, parent ):
    ## Connect to mysql database.
    conn = pymysql.connect( host='127.0.0.1',
                            user='root',
                            passwd='',
                            db='antares_demo' )
    cur = conn.cursor()
    ## Fetch alert replica data
    query = """select * from AlertReplica where ReplicaID={0}""".format( replica_id )
    cur.execute( query )
    replica_row = cur.fetchall()[ 0 ]
    parent_id = replica_row[ 4 ]
    astro_id = replica_row[ 5 ]
    replica_num = replica_row[ 1 ]
    #print( "Parent: {0}, Astro: {1}".format(parent_id, astro_id) )
    parent = ConstructCameraAlertFromID( parent_id )

    #print( parent )
    return AlertReplica( parent, astro_id=astro_id,
                         init_from_db=True, replica_id=replica_id,
                         replica_num=replica_num)

def ConstructAlertFromID( target_id, target_type, parent=None ):
    """
    Generate an alert from the demo database given its ID and type.
    """
    if target_type == 'E':
        return ConstructCameraAlertFromID( target_id )
    if target_type == 'R':
        return ConstructAlertReplicaFromID( target_id, parent )
