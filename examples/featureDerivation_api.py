#!/usr/bin/env python

import sys, os
import numpy as np
import scipy as sp
import scipy.signal as scisig
import scipy.stats as scistats

def derivePeriod( alert ):
    lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( "CA", "Magnitude" )
    times = []
    for time in lightcurve.index.values: # ndarray
        times.append( float(time) )

    timestamps = np.ndarray( lightcurve.index.values.shape,
                             buffer=np.array(times), dtype=float )

    vals       = lightcurve.values # ndarray
    freqs      = np.linspace( 0.01, 10., num=len(vals) )
    period_ind = scisig.lombscargle( timestamps, vals, freqs ).argmax()
    period     = 1./( 2*freqs[period_ind] )

    return period


def deriveAmplitude( alert ):
    lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( "CA", "Magnitude" )
    vals       = lightcurve.values # ndarray
    amp        = np.ptp( vals )
    return amp


def deriveMmed( alert ):
    lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( "CA", "Magnitude" )
    vals       = lightcurve.values # ndarray
    mmed       = np.median(vals)
    return mmed


def deriveKurt( alert ):
    lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( "CA", "Magnitude" )
    vals       = lightcurve.values # ndarray
    kurt       = scistats.kurtosis( vals )
    print( kurt )
    return kurt
    

def deriveStdev(LocusAlert):
    locusid  = LocusAlert.LocusID
    con = mdb.connect('localhost', 'antares', 'br0ker', 'antares_demo');
    with con:
        command = 'SELECT Value from AttributeValue WHERE ContainerID=%i AND AttrName="skew"' %locusid 
        cur = con.cursor()
        cur.execute(command)
        results = cur.fetchall()
        if len(results) == 0:
            timeseries = LocusAlert.assembleTimeSeries_cameraAlerts("CA", "Magnitude")
            vals       = get_vals(timeseries)
            stdev = np.std(vals)
        elif len(results) >= 1:
            stdev =  results[0]
    return stdev


if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateCameraAlertStream
    from antares.helper import ConstructAlertFromID

    ## Construct a camera alert.
    alert_ids = GenerateCameraAlertStream( alert_num=1 )
    alert_id = alert_ids[ 0 ]
    alert = ConstructAlertFromID( alert_id, 'E' )

    replica_id = alert.createReplica()
    print( 'Created replica {0}'.format(replica_id) )

    ## Construct replica object given ID
    replica = ConstructAlertFromID( replica_id, 'R' )

    derivePeriod( replica )
    deriveAmplitude( replica )
    deriveMmed( replica )
    deriveKurt( replica )
