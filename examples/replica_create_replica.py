"""
Example of creating a replica from a replica.
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
    print( alert )

    ## Create a replica with an associated astro object.
    replica_id = alert.createReplica( astro_id=17249 )
    print( 'Created replica {0}'.format(replica_id) )
    ## Construct replica object given ID
    replica = ConstructAlertFromID( replica_id, 'R' )
    print( replica )

    ## Create another replica from the current replica
    replica_replica_id = replica.createReplica()
    print( 'Created replica {0}'.format(replica_replica_id) )

    ## Construct replica object given ID
    replica = ConstructAlertFromID( replica_replica_id, 'R' )
    print( replica )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateCameraAlertStream
    from antares.helper import ConstructAlertFromID
    main()
