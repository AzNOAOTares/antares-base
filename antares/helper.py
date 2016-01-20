"""
Global helper functions.
"""

from antares.model.alert import *
from antares.model.context import *
from antares.model.config import *
import os
import pandas as pd
import pymysql

def GenerateFakeAlerts():
    return [ 777001, 777002, 777003 ]

def GenerateCameraAlertStream( alert_num=10 ):
    """
    Generate a stream of camera alert IDs from the demo database.

    :param int alert_num: the number of camera alerts to be generated.
    :return: a list of camera alert IDs.
    :rtype: list
    """
    ## Connect to mysql database.
    conn = GetDBConn()
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

def CreateCombo( parent_id, replica_ids ):
    conn = GetDBConn()
    cur = conn.cursor()
    query = "select ComboID from Combo"
    cur.execute(query)
    combo_id = len(cur.fetchall())
    sql_insert = """insert into Combo values({0},{1})""".format(combo_id, parent_id)
    cur.execute( sql_insert )

    for replica_id in replica_ids:
        sql_insert = """insert into InCombo(ComboID,ReplicaID) values({0},{1})""".format(combo_id, replica_id)
        cur.execute( sql_insert )

    conn.commit()
    conn.close()

    return combo_id

def ConstructComboFromID( combo_id ):
    conn = GetDBConn()
    cursor = conn.cursor()
    query = "select AlertID from Combo where ComboID={0}".format(combo_id)
    cursor.execute(query)
    alert_id = cursor.fetchall()[0][0]
    print('alert id=', alert_id)
    parent = ConstructCameraAlertFromID(alert_id)
    replicas = []
    query = "select ReplicaID from InCombo where ComboID={0}".format(combo_id)
    cursor.execute(query)
    replica_rows = cursor.fetchall();
    for row in replica_rows:
        replica_id = row[0]
        replica = ConstructAlertReplicaFromID(replica_id)
        replicas.append(replica)

    return AlertCombo(combo_id, parent, replicas)

def ConstructCameraAlertFromID( alert_id ):
    ## Connect to mysql database.
    conn = GetDBConn()
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

def ConstructAlertReplicaFromID( replica_id ):
    ## Connect to mysql database.
    conn = GetDBConn()
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

def ConstructAlertFromID( target_id, target_type ):
    """
    Generate an alert from the demo database given its ID and type.

    :param int target_id: ID of the alert to be constructed.
    :param string target_type: type of the alert to be constructed.
            'E': camera alert, 'R': alert replica.

    :return: :py:class:`antares.alert.Alert` constructed alert object.
    """
    if target_type == 'E':
        return ConstructCameraAlertFromID( target_id )
    if target_type == 'R':
        return ConstructAlertReplicaFromID( target_id )
