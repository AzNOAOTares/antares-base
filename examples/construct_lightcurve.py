"""
Show how to construct a lightcurve(time series of data)
for a camera alert.
"""

#!/usr/bin/env python3

import sys, os

## The main function.
def main():
    alert_ids = GenerateCameraAlertStream(2)
    for alert_id in alert_ids:
        alert = ConstructAlertFromID( alert_id, 'E' )
        lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( 'CA', 'Magnitude' )
        print( lightcurve )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.model.helper import GenerateCameraAlertStream
    from antares.model.helper import ConstructAlertFromID
    main()
