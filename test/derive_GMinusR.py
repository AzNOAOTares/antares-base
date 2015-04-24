"""
Test computation of derived attribute GMinusR.
"""

#!/usr/bin/env python3

import sys, os

## The main function.
def main():
    alerts = GenerateCameraAlertStream()
    for alert in alerts:
        print( alert )
        alert.CA.GMinusR.value = alert.CA.G.value - alert.CA.R.value
        print( alert )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateCameraAlertStream
    main()
