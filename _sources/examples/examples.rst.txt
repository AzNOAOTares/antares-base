***************************************
Examples of using API
***************************************

How to assign/retrieve the value to/from an property
=====================================================

Suppose we have a camera alert ``alert`` with some base properties, for example,
its ``G`` value and ``R`` value, if want to compute the derived
property ``GMinusR`` which belongs to ``CA`` context, we can do::

  from antares.model.alert import CameraAlert

  def computeGMinusR( alert ):
      """'alert' is a camera alert """
      alert.CA.GMinusR.value = alert.CA.G.value - alert.CA.R.value
      alert.CA.GMinusR.confidence = 1.0
      alert.CA.GMinusR.annotation = "High confidence because we don't know"
      alert.CA.GMinusR.description = "G value minus R value"

If ``alert`` does not have ``CA`` context or 
property ``GMinusR`` is not valid under ``CA`` context,
:py:exc:`PropertyError` exception will be raised.
		
Diverting an alert
=====================================================

If we want to divert a camera alert ``alert`` based on the size of
property ``SizeOfLightCurve`` under ``LA`` context, we can do::

  if len( alert.LA.SizeOfLightCurve ) > MAX_LIGHT_CURVE_SIZE:
      alert.divert( "Light curve is too big" )

Creating an alert replica
=========================

If we want to create a replica of a camera alert ``alert`` without
associating an astro object, we can do::

  alert.createReplica()

To associate an astro object ``astro`` when creating a replica, we
do::

  alert.createReplica( astroobj=astro )

Creating a combo based on the value of property ``RedShift``
=============================================================

We can create combos for a camera alert ``alert`` based on the value
of property ``RedShift`` which belongs to ``AR`` context::

  def CreateComboOnRedshift( alert ):
    """
    Create combos based on property redshift. 'alert' is a camera alert.
    """
    if alert.Type != CAMERA_ALERT:
        return

    ## combo forking
    replica_set1 = []
    replica_set2 = []
    for replica in alert.replicas:
        ## group replicas with lower redshift value together
        if replica.AR.RedShift < 0.5:
            replica_set1.append( replica )
        else:
            replica_set2.append( replica )

    if len(replica_set1) > 0:
        alert.CA.createCombo( replica_set1 )
    if len(replica_set2) > 0:
        alert.CA.createCombo( replica_set2 )

Assemble a light curve
======================
If we want to assemble a light curve of a camera alert ``alert``, we
can do::

  lightcurve = alert.LA.assembleTimeSeries_cameraAlerts( "CA", "Magnitude" )


Different ways of iterating property values
============================================

Iterating property values of alert replicas of a camera alert
--------------------------------------------------------------

>>> import numpy as np
>>> values = alert.CA.assembleVector( 'AR', 'Redshift' )
>>> for val in np.nditer( values ):
>>>     print( val )

Here, ``alert`` is a camera alert. The second line of code returns a
numpy array of all the values of property ``Redshift`` under ``AR``
context of replicas of ``alert``.

Iterating property values of alert replicas of an alert combo
--------------------------------------------------------------

>>> import numpy as np
>>> values = combo.CB.assembleVector( 'AR', 'Redshift' )
>>> for val in np.nditer( values ):
>>>     print( val )

Here, ``combo`` is an alert combo. The second line of code returns a
numpy array of all the values of property ``Redshift`` under ``AR``
context of replicas that belongs to ``combo``.

Iterating a time series of all past values an property
-------------------------------------------------------

>>> for item in alert.CA.GMinusR.time_series.iteritems():
>>>     print( item.index, item.value )

Here, ``alert`` is a camera alert. ``alert.CA.GMinusR.time_series`` is
a Pandas time series, so ``item.index`` is a timestamp and
``item.value`` is the actual value of ``GMinusR``.
