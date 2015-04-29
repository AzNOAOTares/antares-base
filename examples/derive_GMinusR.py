"""
Test computation of derived attribute GMinusR.
"""

#!/usr/bin/env python3

import sys, os

## The main function.
def main():
    alerts = GenerateCameraAlertStream()
    for alert in alerts:
        alert.CA.GMinusR.value = alert.CA.G.value - alert.CA.R.value
        alert.CA.GMinusR.confidence = 1.0
        alert.CA.GMinusR.annotation = 'Computed with high confidence'
        print( alert )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateCameraAlertStream
    main()
