"""
Example of committing an alert data to Locus-aggregated Alerts DB.
"""

#!/usr/bin/env python3

import sys, os

import random

def ComputeP():
    return random.random()

## The main function.
def main():
    alert_ids = GenerateCameraAlertStream( alert_num=1 )
    alert_id = alert_ids[ 0 ]

    alert = ConstructAlertFromID( alert_id, 'E' )

    ## Compute P value with lower confidence.
    alert.CA.P.value = ComputeP()
    alert.CA.P.confidence = 0.4
    alert.CA.P.annotation = 'Computed with low confidence'

    #print( alert )

    alert.commit()
    # Second commit won't write DB since everything is synced now.
    alert.commit()

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.model.helper import GenerateCameraAlertStream
    from antares.model.helper import ConstructAlertFromID
    main()
