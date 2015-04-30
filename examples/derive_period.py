"""
Test computation of derived attribute P.
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

    try:
        alert.CA.P.value = 'abc'
    except TypeError:
        print( 'TypeError caught because we are assigning an incompatible type of value!' )

    ## Suppose we first compute P value with lower confidence.
    alert.CA.P.value = ComputeP()
    alert.CA.P.confidence = 0.4
    alert.CA.P.annotation = 'Computed with low confidence'

    ## Later we compute P value with higher confidence, this will
    ## be the most-recently computed value for P. But the previous one
    ## will still be kept with its timpstamp.
    alert.CA.P.value = ComputeP()
    alert.CA.P.confidence = 1.0
    alert.CA.P.annotation = 'Computed with high confidence'

    # This will show the most-recently computed value.
    print( alert )

    # This will print out all the computed values for P and their timestamps.
    print( alert.CA.P.history )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateCameraAlertStream
    from antares.helper import ConstructAlertFromID
    main()
