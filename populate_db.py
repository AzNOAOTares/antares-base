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

path2demo_data = './demo-data'
#debug = True
debug = False

def populate_db( conn, cur ):
    ## Load demo data: PLV LINEAR variable data as a pandas data frame.
    plv_linear_data = pd.read_csv(
        os.path.join(path2demo_data, 'PLV_LINEAR.dat'),
        delimiter=r'\s+' )
    plv_sdss_data = pd.read_csv(
        os.path.join(path2demo_data, 'PLV_SDSS.dat'),
        delimiter=r'\s+' )

    plv_linear_data[ 'RA' ] = plv_sdss_data[ 'RA' ]
    plv_linear_data[ 'Decl' ] = plv_sdss_data[ 'Decl' ]

    ## Populate Attribute table.
    for attrname in CA_base_attributes.keys():
        if CA_base_attributes[attrname][0] == float:
            datatype = 'float'
        else:
            datatype = 'int'
            
        sql_insert = """insert into Attribute values("{0}", 0, "{1}")""".format(
            attrname, datatype )
        cur.execute( sql_insert )

    for attrname in AR_base_attributes.keys():
        if AR_base_attributes[attrname][0] == float:
            datatype = 'float'
        else:
            datatype = 'int'
            
        sql_insert = """insert into Attribute values("{0}", 0, "{1}")""".format(
            attrname, datatype )
        cur.execute( sql_insert )

    for attrname in AO_base_attributes.keys():
        if AO_base_attributes[attrname][0] == float:
            datatype = 'float'
        else:
            datatype = 'int'
            
        sql_insert = """insert into Attribute values("{0}", 0, "{1}")""".format(
            attrname, datatype )
        cur.execute( sql_insert )

    conn.commit()
    
    for index in range( 0, 7194 ):
        ## Fields for Alert table.
        alert_id = plv_linear_data.loc[index, 'LINEARobjectID'].astype(int)
        locus_id = index
        default_decision = 'NA'

        ## Fields for Locus table.
        ra = plv_linear_data.loc[index, 'RA']
        decl = plv_linear_data.loc[index, 'Decl']

        ## Populate Locus table.
        sql_insert = """insert into Locus values({0}, {1}, {2})""".format(locus_id, ra, decl)
        cur.execute( sql_insert )
        ## Populate Locus table.
        sql_insert = """insert into Alert values({0}, "{1}", {2})""".format(alert_id,
                                                                          default_decision,
                                                                          locus_id)
        cur.execute( sql_insert )

        # Open file containing light curve data for 'alert_id'.
        try:
            f = open( os.path.join(path2demo_data, 'lightcurve/'+str(alert_id)+'.dat') )
        except IOError:
            print( "No data file exists for light curve of alert {0}".alert_id )
            exit( -1 )

        ## Fields for AttributeValue table.
        container_id = alert_id
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
            values({0},"{1}","{2}",{3},"",1,"Magnitude")""".format( alert_id, container_type, computed_at, magnitude )
            cur.execute( sql_insert )
            sql_insert = """insert into AttributeValue(ContainerID,ContainerType,ComputedAt,Value,Annotation,Confidence,AttrName)
            values({0},"{1}","{2}",{3},"",1,"MagnitudeErr")""".format( alert_id, container_type, computed_at, magnitude_err )
            cur.execute( sql_insert )

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
