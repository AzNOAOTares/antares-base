#!/usr/bin/env python

import sys, os
import numpy as np
import scipy as sp
import scipy.signal as scisig
import scipy.stats as scistats

def derivePeriod( alert ):
    # If the value of P is already in DB,
    # alert.CA.P.value will return a non-None value.
    period = alert.CA.P.value
    
    if period == None:
        print( 'None period' )
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
    # If the value of A is already in DB,
    # alert.CA.A.value will return a non-None value.
    amp = alert.CA.A.value
    
    if amp == None:
        lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( "CA", "Magnitude" )
        vals       = lightcurve.values # ndarray
        amp        = np.ptp( vals )

    return amp


def deriveMmed( alert ):
    # If the value of mmed is already in DB,
    # alert.CA.mmed.value will return a non-None value.
    mmed = alert.CA.mmed.value
    
    if mmed == None:
        lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( "CA", "Magnitude" )
        vals       = lightcurve.values # ndarray
        mmed       = np.median(vals)

    return mmed


def deriveKurt( alert ):
    # If the value of kurt is already in DB,
    # alert.CA.kurt.value will return a non-None value.
    kurt = alert.CA.kurt.value

    if kurt == None:
        lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( "CA", "Magnitude" )
        vals       = lightcurve.values # ndarray
        kurt       = scistats.kurtosis( vals )

    return kurt
    

def deriveStdev( alert ):
    # If the value of stdev is already in DB,
    # alert.CA.stdev.value will return a non-None value.
    stdev = alert.CA.stdev.value

    if stdev == None:
        lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( "CA", "Magnitude" )
        vals       = lightcurve.values # ndarray
        stdev      = np.std( vals )

    return stdev


if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateFakeAlerts
    from antares.helper import ConstructAlertFromID

    ## Construct a camera alert.
    alert_ids = GenerateFakeAlerts()
    alert_id = alert_ids[ 1 ]
    alert = ConstructAlertFromID( alert_id, 'E' )

    replica_id = alert.createReplica()
    print( 'Created replica {0}'.format(replica_id) )

    ## Construct replica object given ID
    replica = ConstructAlertFromID( replica_id, 'R' )

    replica.CA.P.value = derivePeriod( replica )
    replica.CA.A.value = deriveAmplitude( replica )
    replica.CA.mmed.value = deriveMmed( replica )
    replica.CA.kurt.value = deriveKurt( replica )
    replica.CA.stdev.value = deriveStdev( replica )

    print( 'Replica {0} of camera alert {1}'.format(replica.ID, replica.parent.ID) )
    print( replica.CA.P.value, replica.CA.A.value, replica.CA.mmed.value, replica.CA.stdev.value, replica.CA.kurt.value )
