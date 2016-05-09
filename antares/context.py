"""
Antares context module.
"""

from antares.config import *
from antares.property import *

from io import StringIO
import pymysql
import pandas as pd
from pandas.lib import Timestamp

class Context:
    """
    Represents a context object in general.
    It is the super class for all of the concrete context objects.
    """

    def __init__( self ):
        pass

    def isValidProperty( self, propname ):
        """
        Check whether the given property 'propname' is valid.

        :param string propname: the name of property to be checked

        :return: :py:data:`True` if valid, otherwise :py:data:`False`."""
        pass



class CAContext( Context ):
    """
    Represents a CA (Camera Alert) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under CA context.

    :param: container_id(int): ID of the object that contains the context, which will be a :py:class:`CameraAlert`.
    """
    name = 'CA'
    """
    Name of CA context.

    :type: string
    """

    camera_alert = None
    """
    This is the CameraAlert which contains this CAContext.

    :type: :py:class:`CameraAlert`
    """

    container_type = 'E'

    def __init__( self, container_id ):
        """'container_id' is the ID of the object that owns the context."""
        self.container_id = container_id

        ## Initialize predefined base properties for CA context.
        for propname in CA_base_properties.keys():
            prop = Property( propname, BASE_ATTR, self,
                              CA_base_properties[propname][0], 1,
                              description=CA_base_properties[propname][1] )
            setprop( self, propname, prop )

        ## Initialize predefined derived properties for CA context.
        for propname in CA_derived_properties.keys():
            prop = Property( propname, DERIVED_ATTR, self,
                              CA_derived_properties[propname][0], 1,
                              description=CA_derived_properties[propname][1] )
            setprop( self, propname, prop )

    ## string representation of the CA context object.
    def __str__( self ):
        buf = StringIO()
        buf.write( '{0} Context:\n'.format(self.name) )
        for propname in CA_base_properties.keys():
            prop = getprop( self, propname )
            buf.write( 'Property: {0}, datatype: {1}, value: {2:.2f}\n'
                       .format(prop.name, prop.datatype, prop.value) )

        for propname in CA_derived_properties.keys():
            prop = getprop( self, propname )
            if prop.valueAssigned:
                buf.write( 'Property: {0}, datatype: {1}, value: {2:.2f}, confidence: {3}, annotation: {4}\n'
                           .format(prop.name, prop.datatype, prop.value, prop.confidence, prop.annotation) )

        return buf.getvalue()

    def assembleVector( self, context, propname ):
        """
        The function assembles a vector of all the values of an property inside
        a context of the alert replicas of the camera alert.

        :param string context: the name of the context
        :param string propname: the name of the property

        :return: an array of values
        :rtype: numpy array
        """
        pass


    ## Flush propiubtes under CA to DB if their values is not synced.
    def commit( self, cur ):
        for propname in CA_derived_properties.keys():
            prop = getprop( self, propname )
            if prop.valueAssigned and prop.flushed2DB == False:
                prop.flushed2DB = True
                sql_insert = """insert into PropertyValue(ContainerID,ContainerType,
                ComputedAt,Value, Annotation,Confidence,PropName)
                values({0},"{1}","{2}", {3},"{4}",{5},"{6}")""".format( self.container_id,
                                                                        'E', prop.computedAt, prop.value,
                                                                        prop.annotation, prop.confidence,
                                                                        prop.name )
                cur.execute( sql_insert )
                #print( 'Committing {0}, flushed flag={1}'.format(prop.name, prop.flushed2DB) )

class ARContext( Context ):
    """
    Represents a AR (Alert Replica) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under AR context.

    :param: container_id(int): ID of the object that owns the context, which is a :py:class:`AlertReplica`.
    """
    name = 'AR'
    """Name of AR context."""

    alert_replica = None
    """
    This is the AlertReplica which contains this ARContext.

    :type: :py:class:`AlertReplica`
    """

    def __init__( self, container_id ):
        self.container_id = container_id
        self.container_type = 'R'

        ## Initialize predefined base properties for CA context.
        for propname in AR_base_properties.keys():
            prop = Property( propname, BASE_ATTR, self,
                              AR_base_properties[propname][0], 1,
                              description=AR_base_properties[propname][1] )
            setprop( self, propname, prop )

    def __str__( self ):
        buf = StringIO()
        buf.write( '{0} Context:\n'.format(self.name) )
        for propname in AR_base_properties.keys():
            prop = getprop( self, propname )
            if prop.valueAssigned == True:
                buf.write( 'Property: {0}, datatype: {1}, value: {2:.2f}\n'
                           .format(prop.name, prop.datatype, prop.value) )

        return buf.getvalue()

    ## Flush propiubtes under AR to DB if their values is not synced.
    def commit( self, cur ):
        for propname in AR_base_properties.keys():
            prop = getprop( self, propname )
            if prop.valueAssigned and prop.flushed2DB == False:
                prop.flushed2DB = True
                sql_insert = """insert into PropertyValue(ContainerID,ContainerType,Value, PropName) \
                values({0},"{1}",{2},"{3}")""".format( self.container_id,'R' , prop.value, prop.name )
                cur.execute( sql_insert )
                #print( 'Committing {0}, flushed flag={1}'.format(prop.name, prop.flushed2DB) )

class CBContext( Context ):
    """
    Represents a CB (Alert Combo) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under CB context.
    :param: container_id(int): ID of the object that owns the context, which is a :py:class:`AlertCombo`.
    """
    name = 'CB'
    """
    Name of CB context.

    :type: string
    """

    alert_combo = None
    """
    This is the AlertCombo which contains this CBContext.

    :type: :py:class:`AlertCombo`
    """

    def assembleVector_replicas( self, context, propname ):
        """
        The function assembles a vector of all the values of an property
        inside a context of the alert replicas associated with the alert combo.

        :param string context: the name of the context
        :param string propname: the name of the property

        :return: a list of values
        :rtype: list
        """
        pass


class AOContext( Context ):
    """
    Represents a AO (Astro Object) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under AO context.

    :param: astro_id(int): ID of the :py:class:`AstroObject` that owns the context.
    """
    name = 'AO'
    """
    Name of AO context.

    :type: string
    """

    astro_object = None
    """
    This is the AstroObject which contains this AOContext.

    :type: :py:class:`AstroObject`
    """

    def __init__( self, astro_id ):
        """'continer_id' is the ID of the object that owns the context."""
        self.container_id = astro_id
        self.container_type = 'A'

        ## Initialize predefined base properties for AO context.
        for propname in AO_base_properties.keys():
            prop = Property( propname, BASE_ATTR, self,
                              AO_base_properties[propname][0], 1,
                              description=AO_base_properties[propname][1] )
            setprop( self, propname, prop )

        ## Connect to mysql database.
        conn = GetDBConn()
        cur = conn.cursor()
        query = """select * from PLV_SDSS where object_id={0}""".format(astro_id)
        cur.execute( query )
        row = cur.fetchall()[0]
        for propname in AO_base_properties.keys():
            prop = getprop( self, propname )
            prop.value = row[ AO_base_properties[propname][2] ]

        conn.close()

    def __str__( self ):
        buf = StringIO()
        buf.write( '{0} Context:\n'.format(self.name) )
        for propname in AO_base_properties.keys():
            prop = getprop( self, propname )
            if prop.valueAssigned == True:
                buf.write( 'Property: {0}, datatype: {1}, value: {2:.2f}\n'
                           .format(prop.name, prop.datatype, prop.value) )

        return buf.getvalue()

    ## Flush propiubtes under AR to DB if their values is not synced.
    def commit( self, cur ):
        for propname in AO_base_properties.keys():
            prop = getprop( self, propname )
            if prop.valueAssigned and prop.flushed2DB == False:
                prop.flushed2DB = True
                sql_insert = """insert into PropertyValue(ContainerID,ContainerType,Value, PropName) \
                values({0},"{1}",{2},"{3}")""".format( self.container_id,'O' , prop.value, prop.name )
                cur.execute( sql_insert )
                #print( 'Committing {0}, flushed flag={1}'.format(prop.name, prop.flushed2DB) )


class LAContext( Context ):
    """
    Represents a LA (Locus-aggregated Alert) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under LA context.

    :param: container_id(int): ID of the object (the Alert) that contains the context. **WHAT IS THE CONTAINER?**
    """
    name = 'LA'
    """
    Name of LA context ('LA').

    :type: string
    """

    def __init__( self):
        pass

    def assembleTimeSeriesProperty( self, context, propname, start_time, end_time ):
        """
        The function assembles a time series of all the past values
        of an property inside a context of the camera alerts associated
        with a locus aggregated alert.  Time series may be generated from
        CA, IM, IR, and IS contexts.

        :param string context: the name of the context; valid contexts for this method include the CA, IM, IR, 
        and IS contexts.
        :param string propname: the name of the property

        :return: a time series of values.
        :rtype: :py:class:`pandas.TimeSeries` of (uncertainFloat, string)
        """
        ## Connect to mysql database.
        conn = GetDBConn()
        cur = conn.cursor()

        query = """select ComputedAt, Value from PropertyValue where ContainerID={0} and
        ContainerType="E" and PropName="{1}" """.format( self.container_id, propname )
        cur.execute( query )
        rows = cur.fetchall()
        timestamps = []
        values = []
        for row in rows:
            timestamps.append( Timestamp(row[0]) )
            values.append( row[1] )

        # Return a Pandas TimeSeries
        return pd.Series( values, index=timestamps )


class EAContext( Context ):
    """
    Represents a EA (External Alert) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under EA context.
    """
    name = 'EA'
    """
    Name of EA context.

    :type: string
    """

    external_alert = None
    """
    This is the ExternalAlert which contains this EAContext.

    :type: :py:class:`ExternalAlert`
    """


class IMContext( Context ):
    """
    Represents a IM (Image) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under IM context.
    """
    name = 'IM'
    """
    Name of IM context.

    :type: string
    """

class ISContext( Context ):
    """
    Represents a IS (Image Section) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under IS context.

    :param: container_id(int): ID of the object that contains the context, which is an :py:class:`IMContext`.
    """
    name = 'IS'
    """
    Name of IS context.

    :type: string
    """
    pass

    ir_context = None
    """
    This is the IRContext which contains this ISContext.

    :type: :py:class:`IRContext`
    """

class IRContext( Context ):
    """
    Represents a IR (Image RAFT) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under IR context.
    :param: container_id(int): ID of the object that owns the context, which is an :py:class:`ISContext`.
    """
    name = 'IR'
    """
    Name of IR context.

    :type: string
    """

    im_context = None
    """
    This is the IMContext which contains this IRContext.

    :type: :py:class:`IMContext`
    """

class PSContext( Context ):
    """
    Represents a PS (Point-source AstroObject) context object
    which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under PS context.
    """
    name = 'PS'
    """
    Name of PS context.

    :type: string
    """

    astro_object = None
    """
    This is the AstroObject which contains this PSContext.

    :type: :py:class:`AstroObject`
    """

class ESContext( Context ):
    """
    Represents a ES (Extended-source AstroObject) context object
    which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under ES context.
    """
    name = 'ES'
    """
    Name of ES context.

    :type: string
    """

    astro_object = None
    """
    This is the AstroObject which contains this PSContext.

    :type: :py:class:`AstroObject`
    """

