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


def main( alert ):
    alert.CA.P.value = derivePeriod( alert )
    alert.CA.A.value = deriveAmplitude( alert )
    alert.CA.mmed.value = deriveMmed( alert )
    alert.CA.kurt.value = deriveKurt( alert )
    alert.CA.stdev.value = deriveStdev( alert )

