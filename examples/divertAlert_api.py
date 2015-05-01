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

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateCameraAlertStream
    from antares.helper import ConstructAlertFromID

    alert_ids = GenerateCameraAlertStream( alert_num=2 )
    for alert_id in alert_ids:
        alert = ConstructAlertFromID( alert_id, 'E' )

        replica_id = alert.createReplica()
        replica = ConstructAlertFromID( replica_id, 'R' )
        filterVPDF( replica )
