"""
Antares context module.
"""

#!/usr/bin/env python3

class Context:
    """
    Represents a context object in general. 
    It is the super class for all 11 concrete context objects.    
    """

    def __init__( self ):
        pass

    def isPresent( self ):
        """
        Check if the context is currently present.

        :return: :py:data:`True` if the context is currently present,
                 otherwise :py:data:`False`.
        """
        pass

    def isValidAttribute( self, attrname ):
        """
        Check whether the given attribute 'attrname' is valid.

        :param string attrname: the name of attribute to be checked

        :return: :py:data:`True` if valid, otherwise :py:data:`False`."""
        pass


class CAContext( Context ):
    """
    Represents a CA (Camera Alert) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under CA context.
    """
    name = 'CA'
    """Name of CA context."""
    
    replicas = None
    """A set of the alert replicas created by camera alert."""

    def createReplica( self, astroobj=None ):
        """
        Create an alert replica which is associated with an
        optional astro object ``astroobj``.

        :param: :py:class:`antares.alert.AstroObject` astroobj: the astro object
                to be associated with the created replica.
        """
        replica = AlertReplica( self.alert, astroobj, kind )
        replica.AR.HasAstroObj = True
        replica.AR.ID = self.replicaID
        self.replicaID += 1
        replica.AR.NumberInAlert = self.NumberInAlert
        self.NumberInAlert += 1

    def createCombo( self, replicas ):
        """
        Create an alert combo object which contains a set of
        alert replicas.

        :param list replicas: a set of alert replicas
        """
        pass

    def hasReplicas( self ):
        """
        Check whether alert has replicas.

        :return: :py:data:`True` if alert has replicas, otherwise :py:data:`False`.
        """
        pass

    def assembleVector( self, context, attrname ):
        """
        The function assembles a vector of all the values of an attribute inside
        a context of the alert replicas of the camera alert.

        :param string context: the name of the context
        :param string attrname: the name of the attribute

        :return: a list of values
        :rtype: list
        """
        pass

class ARContext( Context ):
    """
    Represents a AR (Alert Replica) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under AR context.
    """
    name = 'AR'
    """Name of AR context."""
    pass

class CBContext( Context ):
    """
    Represents a CB (Alert Combo) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under CB context.
    """
    name = 'CB'
    """Name of CB context."""
    
    replicas = None
    """A set of the alert replicas associated with the combo."""

    def assembleVector_replicas( self, context, attrname ):
        """
        The function assembles a vector of all the values of an attribute
        inside a context of the alert replicas associated with the alert combo.

        :param string context: the name of the context
        :param string attrname: the name of the attribute

        :return: a list of values
        :rtype: list
        """
        pass

class AOContext( Context ):
    """
    Represents a AO (Astro Object) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under AO context.
    """
    name = 'AO'
    """Name of AO context."""

    pass

class LAContext( Context ):
    """
    Represents a LA (Locus-aggregated Alert) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under LA context.
    """
    name = 'LA'
    """Name of LA context."""

    def assembleTimeSeries_replicas( self, context, attrname ):
        """
        The function assembles a time series of all the past values
        of an attribute inside a context of the alert replicas associated
        with a locus aggregated alert.

        :param string context: the name of the context
        :param string attrname: the name of the attribute

        :return: a time series of values
        :rtype: Pandas TimeSeries
        """
        pass

    def assembleTimeSeries_cameraAlerts( self, context, attrname ):
        """
        The function assembles a time series of all the past values
        of an attribute inside a context of the camera alerts associated
        with a locus aggregated alert.

        :param string context: the name of the context
        :param string attrname: the name of the attribute

        :return: a time series of values
        :rtype: Pandas TimeSeries
        """
        pass

class EAContext( Context ):
    """
    Represents a EA (External Alert) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under EA context.
    """
    name = 'EA'
    """Name of EA context."""
    pass

class IMContext( Context ):
    """
    Represents a IM (Image) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under IM context.
    """
    name = 'IM'
    """Name of IM context."""
    pass

class ISContext( Context ):
    """
    Represents a IS (Image Section) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under IS context.
    """
    name = 'IS'
    """Name of IS context."""
    pass

class IRContext( Context ):
    """
    Represents a IR (Image RAFT) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under IR context.
    """
    name = 'IR'
    """Name of IR context."""
    pass

class PSContext( Context ):
    """
    Represents a PS (Point-source AstroObject) context object
    which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under PS context.
    """
    name = 'PS'
    """Name of PS context."""
    pass

class ESContext( Context ):
    """
    Represents a ES (Extended-source AstroObject) context object
    which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under ES context.
    """
    name = 'ES'
    """Name of ES context."""
    pass
