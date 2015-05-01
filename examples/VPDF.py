#!/usr/bin/env python
"""

"""
import sys
import os
import argparse
import numpy as np

def readKeplerVarTextData():
    midsfile = 'l96b-60.dat.hist.mids'
    ctsfile  = 'l96b-60.dat.hist.counts'
    middata  = np.loadtxt(midsfile, comments='#')
    ctsdata  = np.loadtxt(ctsfile, comments='#')
    histdata =  np.rec.fromarrays([middata,ctsdata], names='mids,cts')
    return histdata


def readKeplerVarData():
    """
    Loads the Kepler Variability data from the files from Tom
    Uses the text file if not saved in binary format (just npz for now)
    Creates the binary file 
    Else, loads from the binary file
    
    """
    npzfile  = 'l96b-60.hist.npz'
    if not os.path.exists(npzfile):
        histdata = readKeplerVarTextData()
        try:
            with open(npzfile, 'w') as f:
                np.savez(f, histdata=histdata)
        except (OSError, IOError) as e:
            # we have histdata at this point anyway
            pass
    else:
        npzdata = np.load(npzfile)
        try:
            histdata = npzdata['histdata']
        except KeyError as e:
            histdata = readKeplerVarTextData()
    return histdata


def scaleKeplerData(ra, dec, histdata):
    """
    Not yet implemented
    In principle this would scale the histogram appropriately for any given ra and dec
    by the stellar distribution from the bezancson model
    """
    return histdata


def findRarity(ra, dec, dmag):
    """
    loads the KeplerVarData, scales it for ra, dec (nyi)
    computes and returns the rarity
    """

    histdata = readKeplerVarData()
    histdata = scaleKeplerData(ra, dec, histdata)
    if dmag > 0. :
        rescts = histdata['cts'][histdata['mids'] >= dmag]
    if dmag <= 0. :
        rescts = histdata['cts'][histdata['mids'] <= dmag]
    rarity = histdata['cts'].sum()/rescts.sum()
    return rarity


def main():
    # TODO: Make this script usable from commandline
    # inputs should be ra, dec, dmag using argparse
    # read in Kepler data
    # scale it for the current position and assess rarity based on dmag
    return


if __name__=='__main__':
    sys.exit(main())

