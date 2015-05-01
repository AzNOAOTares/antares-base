#!/usr/bin/env python
import sys, os
import VPDF

def filterVPDF( alert, rarityThreshold=1E7 ):
    dmag = alert.CA.DeltaMagnitude.value
    ra   = alert.ra
    decl = alert.decl

    rarityVPDF= VPDF.findRarity( ra, decl, dmag )

    if rarityVPDF < rarityThreshold:
        annotation = 'Alert variability less than VPDF threshold (%.2f <  %.2f)' %(rarityVPDF, rarityThreshold)
        print( alert.parent.ID, annotation )
        alert.divert( annotation )

def main( alert ):
    filterVPDF( alert )
