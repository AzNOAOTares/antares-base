"""
Antares context module.
"""

#!/usr/bin/env python3

class Context:
    """
    Represents a context object in general. 
    It is the super class for all concrete context objects.    
    """

    def __init__( self ):
        pass

    def isPresent( self ):
        """Return true is the context is currently present,
        otherwise return false."""
        pass

    def isValidAttribute( self, attrname ):
        """Check whether the given attribute 'attrname' is valid.
        Return true if valid, otherwise false."""
        pass


class CAContext( Context ):
    """
    Represents a CA (Camera Alert) context object which is a sub-class of Context.
    It contains all the attributes defined under CA context.
    """
    name = 'CA'
    """Name of CA context."""
    
    replicas = None
    """A set of the alert replicas created by camera alert."""

    def createReplica( self, astroobj=None ):
        """Create an alert replica which is associated with an
        optional astro object 'astroobj'."""
        replica = AlertReplica( self.alert, astroobj, kind )
        replica.AR.HasAstroObj = True
        replica.AR.ID = self.replicaID
        self.replicaID += 1
        replica.AR.NumberInAlert = self.NumberInAlert
        self.NumberInAlert += 1

    def createCombo( self, replicas ):
        """Create an alert combo object which contains a set of
        alert replicas 'replicas'."""
        pass

    def hasReplicas( self ):
        """Check whether alert has replicas. Return true if alert
        has replicas, otherwise false."""
        pass

    def assembleVector( self, context, attr ):
        """
        The function assembles a vector of all the values of an attribute
        of the alert replicas of the camera alert.
        'attr' is the target attribute and 'context' is where 'attr' belongs.
        """
        pass

class ARContext( Context ):
    """
    Represents a AR (Alert Replica) context object which is a sub-class of Context.
    It contains all the attributes defined under AR context.
    """
    name = 'AR'
    """Name of AR context."""
    pass

class CBContext( Context ):
    """
    Represents a CB (Alert Combo) context object which is a sub-class of Context.
    It contains all the attributes defined under CB context.
    """
    name = 'CB'
    """Name of CB context."""
    
    replicas = None
    """A set of the alert replicas associated with the combo."""

    def assembleVector_replicas( self, context, attr ):
        """
        The function assembles a vector of all the values of an attribute
        of the alert replicas associated with the alert combo.
        'attr' is the target attribute and 'context' is where 'attr' belongs.
        """
        pass

class AOContext( Context ):
    """
    Represents a AO (Astro Object) context object which is a sub-class of Context.
    It contains all the attributes defined under AO context.
    """
    name = 'AO'
    """Name of AO context."""

    pass

class LAContext( Context ):
    """
    Represents a LA (Locus-aggregated Alert) context object which is a sub-class of Context.
    It contains all the attributes defined under LA context.
    """
    name = 'LA'
    """Name of LA context."""

    def assembleTimeSeries_replicas( self, context, attr ):
        """
        The function assembles a time series of all the past values
        of an attribute of the alert replicas associated with a locus aggregated alert.
        'attr' is the target attribute and 'context' is where 'attr' belongs.
        It returns a Pandas TimeSeries.
        """
        pass

    def assembleTimeSeries_cameraAlerts( self, context, attr ):
        """
        The function assembles a time series of all the past values
        of an attribute of the camera alerts associated with a locus aggregated alert.
        'attr' is the target attribute and 'context' is where 'attr' belongs.
        It returns a Pandas TimeSeries.
        """
        pass
