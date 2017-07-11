.. Antares API documentation master file, created by
   sphinx-quickstart on Tue Mar 10 20:02:16 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*************************************************************
Camera Alert ( :py:class:`antares.model.alert.CameraAlert` )
*************************************************************

.. automodule:: antares.model.alert

.. autoclass:: CameraAlert
   :show-inheritance:

   .. rubric:: Attributes Summary

   .. autosummary::

      ~CameraAlert.CA
      ~CameraAlert.LA
      ~CameraAlert.IM
      ~CameraAlert.IR
      ~CameraAlert.IS
      ~CameraAlert.replicas
      ~CameraAlert.combos
      ~CameraAlert.annotation

   .. rubric:: Methods Summary

   .. autosummary::

      ~CameraAlert.createReplica
      ~CameraAlert.createCombo 
      ~CameraAlert.numReplicas 
      ~CameraAlert.throttle
      ~CameraAlert.divert
      ~CameraAlert.mark_as_rare
      ~CameraAlert.hasReplicas

   .. rubric:: Attributes Documentation

   .. autoattribute:: CA
   .. autoattribute:: LA
   .. autoattribute:: IM
   .. autoattribute:: IR
   .. autoattribute:: IS
   .. autoattribute:: replicas
   .. autoattribute:: combos
   .. autoattribute:: annotation

   .. rubric:: Methods Documentation

   .. automethod:: throttle
   .. automethod:: divert
   .. automethod:: createReplica
   .. automethod:: createCombo
   .. automethod:: numReplicas
   .. automethod:: mark_as_rare
