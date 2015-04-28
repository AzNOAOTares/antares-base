"""
Show how to construct a lightcurve(time series of data)
for a camera alert.
"""

#!/usr/bin/env python3

import sys, os

## The main function.
def main():
    alerts = GenerateCameraAlertStream()
    for alert in alerts:
        lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( 'CA', 'Magnitude' )
        print( lightcurve )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateCameraAlertStream
    main()
