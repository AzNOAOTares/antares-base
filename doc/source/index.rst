.. Antares API documentation master file, created by
   sphinx-quickstart on Tue Mar 10 20:02:16 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#################################
Antares Documentation
#################################

.. image:: ./_static/antares.png
   :width: 100px
   :height: 100px

Welcome to Antares documentation.

*************
API reference
*************

Alert related
^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   alert/general_alert
   alert/external_alert
   alert/camera_alert
   alert/alert_replica
   alert/alert_combo
   alert/astroobj

Context related
^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   context/context
   context/ca_context
   context/ar_context
   context/ao_context
   context/la_context
   context/cb_context
   context/ea_context
   context/im_context
   context/is_context
   context/ir_context
   context/ps_context
   context/es_context

Attribute related
^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   attribute/attribute
   attribute/uncertain_float
   attribute/int_pair
   attribute/float_pair
   attribute/prob_curve
   attribute/time_period

Helper functions
^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   helper/index

Pre-defined Attribute
^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2

   attribute/predefined

*************************
Class inheritance diagram
*************************

.. image:: ./_static/classes.png
   :width: 500px
   :height: 480px

Class inheritance relationship
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:py:class:`antares.alert.Alert` is the superclass for
:py:class:`antares.alert.CameraAlert` and 
:py:class:`antares.alert.ExternalAlert`.

:py:class:`antares.alert.CameraAlert` is the superclass for
:py:class:`antares.alert.AlertReplica` and
:py:class:`antares.alert.AlertCombo`.

:py:class:`antares.context.Context` is the superclass for the other 11
context classes.

Class composition relationship
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An :py:class:`antares.alert.ExternalAlert` has exactly one
:py:class:`antares.context.Context`, which is :py:class:`antares.context.EAContext`.

A :py:class:`antares.alert.CameraAlert` has one to many
:py:class:`antares.context.Context`.

A :py:class:`antares.context.Context` has one to many :py:class:`antares.attribute.Attribute`.

*********************
Rules & Constraints
*********************

.. toctree::
   :maxdepth: 2

   rules_constraints.rst

*********************
Examples
*********************

.. toctree::
   :maxdepth: 2

   examples/examples.rst

************************
Assumptions and Comments
************************
* The alerts (and combos and replicas) can be processed entirely in parallel and entirely independently of one another.

NOTE: we decided to leave for later discussion the identification of structures of camera alerts within an image (e.g., a cluster of say 100 alerts within a small area). We can incorporate such identification as a separate analysis, outside that of the stages.

* Each alert within a stage will read one or more attributes from multiple contexts (e.g., Image, RAFT, Section, AstroObject, Camera Alert, Locus-Aggregated Alert) relevant only for that alert.

* Values of an attribute in a larger context (e.g., Image) will be the same across the relevant alerts (e.g., for every alert in that Image, for every alert in that RAFT).

* Each alert within a stage will write a new value for one or more attributes within multiple contexts.

* Values cannot be written for a larger context (e.g., Image) within an alert stage. So a camera alert can write to attributes in the CA context but not to the Image or AstroObject contexts.

Note: the Antares Data Model document (https://docs.google.com/document/d/1xjYmhd8W9pyiwCBLA6o8mJeAz99Qbz9NvYFpICvYfSA/) had an example of

`LA-LightCurve = F2( LA-CameraAlerts.TimeSeries(CA-Brightness),
                                        CA-Brightness, CA-Time )`

Such an assignment would be allowed within a camera alert, because a Locus-Aggregated Alert (LA) has exactly one Camera Alert (CA) at any time. However, that would not be allowed within a replica or combo.

NOTE: We discussed computing something like the count of the number of alerts by allowing something like

IM-CountAlerts =+ 1;

which reads IM-CountAlerts, adds one, and writes it. That is explicitly forbidden above. However, for such *accumulative* calculations, there may be ways to incorporate them by having a separate process that accepts such accumulations and coalesces them into a single assignment, rather than a complex sequence of parallel reads and write, which we want to avoid allowing.

* Written values are stored in the database only when a stage completes. A stage that is aborted loses those values, because the stage was incomplete.

* An attribute can be written to multiple times in a stage or in separate stages, but only the last value will be visible for a particular camera alert. (We allow this because different astronomers might have independently written different stages.)

* The values form a time series, one value computed for each alert at that time. Hence, old values are retained and the new value extends the time series. No value is ever changed in the database (except for multiple writes, discussed above, which we can finesse.)

* There will be a separate conversion process that will translate the highly-optimized storage structure used in the ANTARES pipeline (a linear sequence of name-value blocks stored contiguously for each locus-aggregated alert) to and from the traditional relational structure as described in the ER diagram. The latter representation will be best for cross-alert analyses. The conversion(s) and cross-alert analyses will happen outside the time-critical portion of ANTARES and may be challenging in their own way in terms of performance.User-contributed stages write to attributes associated with a context of the current alert. So a single stage or multiple stages could successively write to the same attribute, changing its value as the processing pipeline progresses. We retain the value as of the end of each stage, but a future alert at the same locus will only see the final value of that attribute: there is no facility for seeing an intermediate value within a stage or between stages of a single past alert at that locus.

* User-contributed stages can also write to local variables during their processing, but such variables will not be persisted between stages. The only values that are persisted are those associated with the contexts of the alert.

******************
Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

