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

    ## Load demo data: PLV LINEAR variable data as a pandas data frame.
    plv_linear_data = pd.read_csv( os.path.join(path2demo_data, 'PLV_LINEAR.dat'),
                                   delimiter=r'\s+' )

    for index in range( 0, 7194 ):
        alert_id = plv_linear_data.loc[index, 'LINEARobjectID'].astype(int)

        container_type = 'E'

        ## Fields of derived attributes
        for attrname in CA_derived_attributes.keys():
            val = plv_linear_data.loc[ index, attrname ]
            sql_insert = """insert into AttributeValue(ContainerID,ContainerType,Value,AttrName)
            values({0},"{1}",{2},"{3}")""".format( alert_id, container_type, val, attrname )
            cur.execute( sql_insert )

            print( 'injecting derived attributes for alert {0}.'.format(alert_id) )
            #print( 'Alert: {0} with {1}={2}'.format(alert_id, attrname, val) )

    conn.commit()

## The main function.
def main():
    ## Connect to mysql database.
    conn = pymysql.connect( host='127.0.0.1',
                            user='root',
                            passwd='',
                            db='antares_demo' )
    cur = conn.cursor()
    update_db( conn, cur )
    

if __name__ == '__main__':
    main()
