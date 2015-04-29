"""
Test camera alert stream generation.
"""

#!/usr/bin/env python3

import sys, os

## The main function.
def main():
    alerts = GenerateCameraAlertStream( alert_num=5 )
    for alert in alerts:
        print( alert )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares import GenerateCameraAlertStream
    main()
