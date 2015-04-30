#!/usr/bin/env python
import VPDF

def filterVPDF(CameraAlert, rarityThreshold=1E7):
    dmag      = CameraAlert.DeltaMag
    position  = CameraAlert.LA.position()
    ra, dec   = position
    rarityVPDF= VPDF.findRarity(ra, dec, dmag)

    if rarityVPDF < rarityThreshold:
        anotation = 'Alert variability less than VPDF threshold (%.2f <  %.2f)' %(rarityVPDF, rarityThreshold)
        CameraAlert.divert(anotation)
