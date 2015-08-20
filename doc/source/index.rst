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

******************
Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

