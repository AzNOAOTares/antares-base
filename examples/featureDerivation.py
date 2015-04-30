#!/usr/bin/env python

import numpy as np
import scipy as sp
import scipy.signal as scisig
import scipy.stats as scistats
import astropy.coordinates as coords
import MySQLdb as mdb


def derivePeriod(LocusAlert):
    locusid  = LocusAlert.LocusID
    con = mdb.connect('localhost', 'antares', 'br0ker', 'antares_demo')
    with con:
        command = 'SELECT Value from AttributeValue WHERE ContainerID=%i AND AttrName="P"' %locusid 
        cur = con.cursor()
        cur.execute(command)
        results = cur.fetchall()
        if len(results) == 0:
            timeseries = LocusAlert.assembleTimeSeries_cameraAlerts("CA", "Magnitude")
            timestamp  = get_times(timeseries)
            vals       = get_vals(timeseries)
            freq       = np.linspace(0.01, 10., 0.01)
            period_ind = scisig.lomb_scargle(timestamp, vals, freq).argmax()
            period     = 1./(2*freq[period_ind])
        elif len(results) >= 1:
            period =  results[0]
    return period





def deriveAmplitude(LocusAlert):
    locusid  = LocusAlert.LocusID
    con = mdb.connect('localhost', 'antares', 'br0ker', 'antares_demo');
    with con:
        command = 'SELECT Value from AttributeValue WHERE ContainerID=%i AND AttrName="A"' %locusid 
        cur = con.cursor()
        cur.execute(command)
        results = cur.fetchall()
        if len(results) == 0:
            timeseries = LocusAlert.assembleTimeSeries_cameraAlerts("CA", "Magnitude")
            vals       = get_vals(timeseries)
            amp = np.ptp(vals)
        elif len(results) >= 1:
            amp =  results[0]
    return amp





def deriveMmed(LocusAlert):
    locusid  = LocusAlert.LocusID
    con = mdb.connect('localhost', 'antares', 'br0ker', 'antares_demo');
    with con:
        command = 'SELECT Value from AttributeValue WHERE ContainerID=%i AND AttrName="mmed"' %locusid 
        cur = con.cursor()
        cur.execute(command)
        results = cur.fetchall()
        if len(results) == 0:
            timeseries = LocusAlert.assembleTimeSeries_cameraAlerts("CA", "Magnitude")
            vals       = get_vals(timeseries)
            mmed = np.median(vals)
        elif len(results) >= 1:
            mmed =  results[0]
    return mmed



def deriveKurt(LocusAlert):
    locusid  = LocusAlert.LocusID
    con = mdb.connect('localhost', 'antares', 'br0ker', 'antares_demo');
    with con:
        command = 'SELECT Value from AttributeValue WHERE ContainerID=%i AND AttrName="kurt"' %locusid 
        cur = con.cursor()
        cur.execute(command)
        results = cur.fetchall()
        if len(results) == 0:
            timeseries = LocusAlert.assembleTimeSeries_cameraAlerts("CA", "Magnitude")
            vals       = get_vals(timeseries)
            kurt = scistat.kurtosis(vals)
        elif len(results) >= 1:
            kurt =  results[0]
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
