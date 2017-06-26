"""
Examples of how to access RA and Decl for a camera alert.
"""

import sys, os

## The main function.
def main():
    alert_ids = GenerateCameraAlertStream( alert_num=5 )
    for alert_id in alert_ids:
        alert = ConstructAlertFromID( alert_id, 'E' )
        
        ## This is the recommended way of getting ra/dec for an alert:
        ## directly from alert.
        ra = alert.ra
        decl = alert.decl
        print( 'alert {0}: ra={1}, dec={2}'.format(alert.ID, ra, decl) )

        ## This is not recommended: too verbose and multiple level of references.
        ra = alert.CA.RA.value
        decl = alert.CA.Decl.value
        print( 'alert {0}: ra={1}, dec={2}'.format(alert.ID, ra, decl) )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.model.helper import GenerateCameraAlertStream
    from antares.model.helper import ConstructAlertFromID
    main()
