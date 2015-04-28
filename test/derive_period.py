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
    alerts = GenerateCameraAlertStream()
    for alert in alerts:
        alert.CA.P.value = ComputeP()
        alert.CA.P.confidence = 1.0
        alert.CA.P.annotation = 'Computed with high confidence'
        print( alert )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateCameraAlertStream
    main()
