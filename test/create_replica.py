"""
Example of creating an alert replica.
"""

#!/usr/bin/env python3

import sys, os

import random

def ComputeP():
    return random.random()

## The main function.
def main():
    alerts = GenerateCameraAlertStream( alert_num=1 )
    alert = alerts[ 0 ]

    ## Create a replica with an associated astro object.
    replica1 = alert.createReplica( astro_id=17249 )
    print( replica1 )
    replica1.commit() # flush replica data to DB
    replica1.commit() # second commit won't work since it is already synced with DB.

    ## Create another replica without an associated astro object.
    replica2 = alert.createReplica()
    print( replica2 )
    replica2.commit() # flush replica data to DB
    replica2.commit() # second commit won't work since it is already synced with DB.

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateCameraAlertStream
    main()
