"""
Test camera alert stream generation.
"""

#!/usr/bin/env python3

import sys, os

## The main function.
def main():
    alert_ids = GenerateFakeAlerts()
    for alert_id in alert_ids:
        print( alert_id )
        alert = ConstructAlertFromID( alert_id, 'E' )
        print( alert )
        lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( 'CA', 'Magnitude' )
        print( lightcurve )
        print( 'P=', alert.CA.P.value )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateFakeAlerts
    from antares.helper import ConstructAlertFromID
    main()
