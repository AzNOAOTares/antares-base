"""
Global helper functions.
"""

#!/usr/bin/env python3

from antares.alert import *
from antares.context import *
from antares.config import *
import os
import pandas as pd

def GenerateCameraAlertStream( alert_num=10, night=1 ):
    """
    Randomly generate a stream of camera alerts from
    the demo data.
    """
    if night < 1:
        print( "The value of 'night' must be greater than 0!" )
        exit( -1 )

    if night*alert_num > total_num_alerts:
        print( 'We have reached the limit of camera alert we can generate!' )
        exit( -1 )
    
    ## load demo data: PLV LINEAR variable data as a pandas data frame.
    plv_linear_data = pd.read_csv( os.path.join(demo_data_path, 'PLV_LINEAR.dat'),
                                   delimiter=r'\s+' )
    plv_sdss_data = pd.read_csv( os.path.join(demo_data_path, 'PLV_SDSS.dat'),
                                 delimiter=r'\s+' )
    plv_linear_data[ 'RA' ] = plv_sdss_data[ 'RA' ]
    plv_linear_data[ 'Decl' ] = plv_sdss_data[ 'Decl' ]
    plv_linear_data[ 'g' ] = plv_sdss_data[ 'g' ]
    plv_linear_data[ 'r' ] = plv_sdss_data[ 'r' ]

    alerts = [] # list of camera alerts to be returned to caller.
    for index in range( alert_num*(night-1), alert_num*night ):
        ca_context = CAContext()
        for attrname in CA_attributes.keys():
            attr = getattr( ca_context, attrname )
            attr.value = plv_linear_data.loc[index, attrname].astype(attr.datatype)

        alert_id = plv_linear_data.loc[index, 'LINEARobjectID'].astype(int)
        ra = plv_linear_data.loc[index, 'RA']
        decl = plv_linear_data.loc[index, 'Decl']
        alert = CameraAlert( alert_id, ra, decl, ca_context, None, None, None, None )
        alerts.append( alert )

    return alerts # return the generated camera alert stream
