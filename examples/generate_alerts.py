"""
Test camera alert stream generation.
"""

#!/usr/bin/env python3

import sys, os

## The main function.
def main():
    alert_ids = GenerateCameraAlertStream( alert_num=5 )
    for alert_id in alert_ids:
        print( alert_id )
        alert = ConstructAlertFromID( alert_id, 'E' )
        print( alert )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares import GenerateCameraAlertStream
    from antares import ConstructAlertFromID
    main()
