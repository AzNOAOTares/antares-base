"""
Global helper functions.
"""

from antares.model.alert import *
from antares.model.context import *
from antares.model.config import *
import os
import pandas as pd
import pymysql
from datetime import datetime

import antares.stage_algorithms.ANTARES_object as ANTARES_object

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
        query = """select Value from PropertyValue where ContainerID={0} \
        and ContainerType='E' and propname='DeltaMagnitude'""".format(alert_id)
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

    pband = None
    for band in ['u','g','r','i','z','v']:
        query = """select * from PropertyValue where ContainerID={} and
        ContainerType="E" and PropName="{}" limit 1""".format( alert_id, band+'MAG')
        cur.execute( query )
        rows = cur.fetchall()
        if len(rows) > 0:
            pband = band
            break

    query = """select Value from PropertyValue where ContainerID={0} and
    ContainerType="E" and PropName="MJDOBS" """.format( alert_id )
    cur.execute( query )
    rows = cur.fetchall()
    MJDOBS = rows[0][0]

    query = """select Value from PropertyValue where ContainerID={0} and
    ContainerType="E" and PropName="{1}" """.format( alert_id, pband+'MAG')
    cur.execute( query )
    mag_rows = cur.fetchall()
    # The most-recenctly computed magnitude value.
    magnitude = None
    if len(mag_rows) > 0:
        magnitude = mag_rows[len(mag_rows)-1][0]

    query = """select Value from PropertyValue where ContainerID={0} and
    ContainerType="E" and PropName="{1}" """.format( alert_id, pband+'MAGERR')
    cur.execute( query )
    magerr_rows = cur.fetchall()
    # The most-recenctly computed magnitude value.
    magnitude_err = 0
    if len(magerr_rows) > 0:
        magnitude_err = magerr_rows[len(magerr_rows)-1][0]

    query = """select Value from PropertyValue where ContainerID={0} and
    ContainerType="E" and PropName="{1}" """.format( alert_id, pband+'Ref_mag' )
    cur.execute( query )
    delta_mag_rows = cur.fetchall()
    # The most-recenctly computed magnitude value.
    delta_magnitude = None
    if len(delta_mag_rows) > 0:
        delta_magnitude = magnitude - delta_mag_rows[0][0]

    ca_context.Magnitude.value = magnitude
    ca_context.MagnitudeErr.value = magnitude_err
    if delta_magnitude is not None:
        ca_context.DeltaMagnitude.value = delta_magnitude
    #print( alert_id, ra, decl, magnitude, magnitude_err )
    #print( type(magnitude) )

    alert = CameraAlert( alert_id, ra, decl, ca_context, decision, locus_id )
    alert.MJDOBS = MJDOBS
    alert.passband = pband

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
    conn.close()
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
    if target_type == 'C':
        return ConstructComboFromID( target_id )

def CreateCameraAlerts(alerts):
    conn = GetDBConn()
    cur = conn.cursor()

    # Get the alert id base
    sql = """SELECT count(*) FROM Alert"""
    cur.execute(sql)
    AID = cur.fetchall()[0][0]

    ids = []
    for alert in alerts:
        AID += 1
        alert_id = AID

        # Get HtmID as LocusID
        sql = "SELECT scisql_s2HtmId({}, {}, 20)".format(alert['ra'], alert['decl'])
        cur.execute(sql)
        htmID = cur.fetchall()[0][0]

        # Insert into Locus
        sql = """INSERT IGNORE INTO Locus VALUES
                 ({}, {}, {})""".format(htmID, alert['ra'], alert['decl'])
        cur.execute(sql)

        # Insert into Alert
        sql = """INSERT INTO Alert VALUES
                 ({}, "{}", {}, "{}")""".format(alert_id, 'NA', htmID, 'NA')
        cur.execute(sql)

        ids.append(alert_id)

    conn.close()
    return ids

def savePropInDB(container_ID, container_Type, prop_name, prop_value):
    conn = GetDBConn()
    cur = conn.cursor()

    computetime = datetime.now().timestamp()

    query = """insert into PropertyValue(ContainerID, ContainerType, ComputedAt, Value, PropName)
            values({}, "{}", {}, {}, "{}")"""\
            .format(container_ID, container_Type, computetime, prop_value, prop_name)
    cur.execute(query)
    conn.commit()
    conn.close()

def MakeTouchstoneObject(alert):
        
    return assembleFullTimeSeries(alert)


def ConstructAlerts(alertlist):
    conn = GetDBConn()
    cur = conn.cursor()
    alertIDs = []

    for data in alertlist:
        # TODO we should generate a unique id for each alert
        alertID = data['id']
        alertIDs.append(alertID)

        computetime = datetime.now().timestamp()

        ## Fields for Locus table.
        ra = float(data['RA'])
        decl = float(data['DECL'])
        sql = "SELECT scisql_s2HtmId({}, {}, 20)".format(ra, decl)
        cur.execute(sql)
        locus_id = cur.fetchall()[0][0]

        ## Populate Alert table.
        sql_insert = """insert ignore into Alert values({0}, "NA", {1}, "NULL")""".format(alertID, locus_id)
        cur.execute( sql_insert )

        ## Populate Locus table.
        sql_insert = """insert ignore into Locus values({0}, {1}, {2})""".format(locus_id, ra, decl)
        cur.execute( sql_insert )

        ## Insert Properties
        if "Ref_mag" in data:
            sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"E",{},"{}","{}")""".format(alertID, data['Ref_mag'], data['passband']+'Ref_mag',data['MJDOBS'])
            cur.execute(sql_insert)

        sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"E",{},"{}","{}")""".format(alertID, data['MAG'], data['passband']+'MAG',data['MJDOBS'])
        cur.execute(sql_insert)

        sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"E",{},"{}","{}")""".format(alertID, data['MAGERR'], data['passband']+'MAGERR',data['MJDOBS'])
        cur.execute(sql_insert)

        sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"E",{},"{}","{}")""".format(alertID, data['MJDOBS'], 'MJDOBS', data['MJDOBS'])
        cur.execute(sql_insert)

        if "IMAGEX" in data:
            sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"E",{},"{}","{}")""".format(alertID, data['IMAGEX'], 'IMAGEX', data['MJDOBS'])
            cur.execute(sql_insert)

        if "IMAGEY" in data:
            sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"E",{},"{}","{}")""".format(alertID, data['IMAGEY'], 'IMAGEY', data['MJDOBS'])
            cur.execute(sql_insert)

        if "PSF" in data:
            sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"E",{},"{}","{}")""".format(alertID, data['PSF'], 'PSF', data['MJDOBS'])
            cur.execute(sql_insert)

        if "FLUX" in data:
            sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"E",{},"{}","{}")""".format(alertID, data['FLUX'], 'FLUX', data['MJDOBS'])
            cur.execute(sql_insert)
        if "FLUXERR" in data:
            sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"E",{},"{}","{}")""".format(alertID, data['FLUXERR'], 'FLUXERR', data['MJDOBS'])
            cur.execute(sql_insert)

        
        # Insert as Locus aggregated data
        # sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"L",{},"{}","{}")""".format(locus_id, data['Ref_mag'], data['passband']+'Ref_mag',data['MJDOBS'])
        # cur.execute(sql_insert)

        # sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"L",{},"{}","{}")""".format(locus_id, data['MAG'], data['passband']+'MAG',data['MJDOBS'])
        # cur.execute(sql_insert)

        # sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"L",{},"{}","{}")""".format(locus_id, data['MAGERR'], data['passband']+'MAGERR',data['MJDOBS'])
        # cur.execute(sql_insert)

        # sql_insert = """insert into PropertyValue (ContainerID, ContainerType,Value,PropName, ComputedAt) values({},"L",{},"{}","{}")""".format(locus_id, data['MJDOBS'], 'MJDOBS', data['MJDOBS'])
        # cur.execute(sql_insert)

    conn.commit()
    conn.close()
    return alertIDs

def assembleFullTimeSeries(alert):
    
    filters = ['u','g','r','i','z','v']
    mag  = []
    dmag = []
    time = []
    passband = []
    for pb in filters:
        thispbmagvec  = alert.LA.assembleProperties('%sMAG'%pb)
        thispbdmagvec = alert.LA.assembleProperties('%sMAGERR'%pb)
        if thispbmagvec is None:
            continue
        elif len(thispbmagvec) == 0:
            continue
        
        tpbtime1, tpbmag , __ = zip(*thispbmagvec)
        tpbtime2, tpbdmag, __ = zip(*thispbdmagvec)

        tpbtime1 = np.array(tpbtime1)
        tpbtime2 = np.array(tpbtime2)
        tpbmag = np.array(tpbmag)
        tpbdmag = np.array(tpbdmag)

        m1 = np.argsort(tpbtime1)
        m2 = np.argsort(tpbtime2)

        time  += tpbtime1[m1].tolist()
        mag   += tpbmag[m1].tolist()
        dmag  += tpbdmag[m2].tolist()
        passband    += np.repeat(pb, len(tpbtime1)).tolist()
    mag  = np.array(mag)
    dmag = np.array(dmag)
    time = np.array(time)
    passband = np.array(passband)
    objid = alert.LA.container_id
    tobj  = ANTARES_object.TouchstoneObject(objid, time, mag, dmag, passband, flux=False) 
    return tobj
