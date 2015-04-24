"""
Antares context module.
"""

#!/usr/bin/env python3
from antares.config import *
from antares.attribute import *
from io import StringIO

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
    """
    Name of CA context.

    :type: string
    """
    
    replicas = None
    """
    A set of the alert replicas created by camera alert.

    :type: list
    """

    def __init__( self ):
        ## Initialize predefined attributes for CA context.
        for attrname in CA_attributes.keys():
            attr = Attribute( attrname, 'CA', CA_attributes[attrname][0],
                              1, description=CA_attributes[attrname][1] )
            setattr( self, attrname, attr )

    ## string representation of the CA context object.
    def __str__( self ):
        buf = StringIO()
        buf.write( '{0} Context:\n'.format(self.name) )
        for attrname in CA_attributes.keys():
            attr = getattr( self, attrname )
            buf.write( 'Attribute: {0}, datatype: {1}, value: {2}\n'
                       .format(attr.name, attr.datatype, attr.value) )
        return buf.getvalue()

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

        :return: an array of values
        :rtype: numpy array
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
    """
    Name of CB context.

    :type: string
    """
    
    replicas = None
    """
    A set of the alert replicas associated with the combo.

    :type: list
    """

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
    """
    Name of AO context.

    :type: string
    """

    pass

class LAContext( Context ):
    """
    Represents a LA (Locus-aggregated Alert) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under LA context.
    """
    name = 'LA'
    """
    Name of LA context.

    :type: string
    """

    def assembleTimeSeries_replicas( self, context, attrname ):
        """
        The function assembles a time series of all the past values
        of an attribute inside a context of the alert replicas associated
        with a locus aggregated alert.

        :param string context: the name of the context
        :param string attrname: the name of the attribute

        :return: a time series of values. Here the value is a dict that maps
                 replica ID to the real value of ``attrname``.
        :rtype: :py:class:`pandas.Series`
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
    """
    Name of EA context.

    :type: string
    """
    pass

class IMContext( Context ):
    """
    Represents a IM (Image) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under IM context.
    """
    name = 'IM'
    """
    Name of IM context.

    :type: string
    """
    pass

class ISContext( Context ):
    """
    Represents a IS (Image Section) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under IS context.
    """
    name = 'IS'
    """
    Name of IS context.

    :type: string
    """
    pass

class IRContext( Context ):
    """
    Represents a IR (Image RAFT) context object which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under IR context.
    """
    name = 'IR'
    """
    Name of IR context.

    :type: string
    """
    pass

class PSContext( Context ):
    """
    Represents a PS (Point-source AstroObject) context object
    which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under PS context.
    """
    name = 'PS'
    """
    Name of PS context.

    :type: string
    """
    pass

class ESContext( Context ):
    """
    Represents a ES (Extended-source AstroObject) context object
    which is a sub-class of :py:class:`Context`.
    It contains all the attributes defined under ES context.
    """
    name = 'ES'
    """
    Name of ES context.

    :type: string
    """
    pass
