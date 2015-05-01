"""
Example of showing how to mark an alert as a rare alert.
"""

#!/usr/bin/env python3

import sys, os

## The main function.
def main():
    alert_ids = GenerateCameraAlertStream( alert_num=1 )
    alert_id = alert_ids[ 0 ]

    alert = ConstructAlertFromID( alert_id, 'E' )
    print( alert )

    ## Create a replica with an associated astro object.
    replica_id1 = alert.createReplica( astro_id=17249 )
    print( 'Created replica {0}'.format(replica_id1) )
    ## Construct replica object given ID
    replica1 = ConstructAlertFromID( replica_id1, 'R' )
    replica1.mark_as_rare( 'Replica1 is rare' )

    ## Create another replica without an associated astro object.
    replica_id2 = alert.createReplica()
    print( 'Created replica {0}'.format(replica_id2) )

    ## Construct replica object given ID
    replica2 = ConstructAlertFromID( replica_id2, 'R' )
    replica2.mark_as_rare( 'Replica2 is rare' )

    print( alert.get_annotation() )

if __name__ == '__main__':
    sys.path.append( '../' )
    from antares.helper import GenerateCameraAlertStream
    from antares.helper import ConstructAlertFromID
    main()
