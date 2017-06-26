"""
Antares context module.
"""

from antares.model.config import *
from antares.model.property import *
from io import StringIO
import pymysql
import pandas as pd
from pandas.lib import Timestamp
from datetime import datetime
import time
import numpy as np

class Context:
    """
    Represents a context object in general.
    It is the super class for all 11 concrete context objects.
    """

    def __init__( self ):
        pass

    def isValidProperty( self, propertyname ):
        """
        Check whether the given Property 'propertyname' is valid.

        :param string propertyname: the name of propname to be checked

        :return: :py:data:`True` if valid, otherwise :py:data:`False`."""
        pass


class CAContext( Context ):
    """
    Represents a CA (Camera Alert) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under CA context.

    :param: container_id(int): ID of the object that owns the context.
    """
    name = 'CA'
    """
    Name of CA context.

    :type: string
    """

    container_type = 'E'

    def __init__( self, container_id ):
        """'container_id' is the ID of the object that owns the context."""
        self.container_id = container_id

        ## Initialize predefined base Properties for CA context.
        for propname in CA_base_properties.keys():
            prop = Property( propname, BASE_PROP, self,
                              CA_base_properties[propname][0], 1,
                              description=CA_base_properties[propname][1] )
            setattr( self, propname, prop )

        ## Initialize predefined derived properties for CA context.
        for propname in CA_derived_properties.keys():
            prop = Property( propname, DERIVED_PROP, self,
                              CA_derived_properties[propname][0], 1,
                              description=CA_derived_properties[propname][1] )
            setattr( self, propname, prop )

    ## string representation of the CA context object.
    def __str__( self ):
        buf = StringIO()
        buf.write( '{0} Context:\n'.format(self.name) )
        for propname in CA_base_properties.keys():
            prop = getattr( self, propname )
            buf.write( 'Property: {0}, datatype: {1}, value: {2:.2f}\n'
                       .format(prop.name, prop.datatype, prop.value) )

        for propname in CA_derived_properties.keys():
            prop = getattr( self, propname )
            if prop.valueAssigned:
                buf.write( 'Property: {0}, datatype: {1}, value: {2:.2f}, confidence: {3}, annotation: {4}\n'
                           .format(prop.name, prop.datatype, prop.value, prop.confidence, prop.annotation) )

        return buf.getvalue()

    def assembleVector( self, context, propname ):
        """
        The function assembles a vector of all the values of an Property inside
        a context of the alert replicas of the camera alert.

        :param string context: the name of the context
        :param string propname: the name of the Property

        :return: an array of values
        :rtype: numpy array
        """
        conn = GetDBConn()
        cursor = conn.cursor()

        v = []

        # TODO: check if propname is in context
        query = """SELECT Value from PropertyValue
                       where PropName="{}" and ContainerID in
                   (SELECT ReplicaID from AlertReplica
                       where AlertID={})""".format(propname, self.container_id)
        cursor.execute(query)
        results = cursor.fetchall()
        v = [i[0] for i in results]

        conn.close()
        return np.array(v)

    ## Flush propiubtes under CA to DB if their values is not synced.
    def commit( self, cur ):
        for propname in CA_derived_properties.keys():
            prop = getattr( self, propname )
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

    :param: container_id(int): ID of the object that owns the context.
    """
    name = 'AR'
    """Name of AR context."""

    def __init__( self, container_id ):
        self.container_id = container_id
        self.container_type = 'R'

        ## Initialize predefined base properties for CA context.
        for propname in AR_base_properties.keys():
            prop = Property( propname, BASE_PROP, self,
                              AR_base_properties[propname][0], 1,
                              description=AR_base_properties[propname][1] )
            setattr( self, propname, prop )

    def __str__( self ):
        buf = StringIO()
        buf.write( '{0} Context:\n'.format(self.name) )
        for propname in AR_base_properties.keys():
            prop = getattr( self, propname )
            if prop.valueAssigned == True:
                buf.write( 'Property: {0}, datatype: {1}, value: {2:.2f}\n'
                           .format(prop.name, prop.datatype, prop.value) )

        return buf.getvalue()

    ## Flush propiubtes under AR to DB if their values is not synced.
    def commit( self, cur ):
        for propname in AR_base_properties.keys():
            prop = getattr( self, propname )
            if prop.valueAssigned and prop.flushed2DB == False:
                prop.flushed2DB = True
                sql_insert = """insert into PropertyValue(ContainerID,ContainerType,Value, PropName, ComputedAt, Annotation) \
                values({0},"{1}",{2},"{3}", "{4}", "{5}")""".format( self.container_id,'R' , prop.value, prop.name, time.time(), prop.annotation )
                cur.execute( sql_insert )
                #print( 'Committing {0}, flushed flag={1}'.format(prop.name, prop.flushed2DB) )

class CBContext( Context ):
    """
    Represents a CB (Alert Combo) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under CB context.
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

    def assembleVector_replicas( self, context, propname ):
        """
        The function assembles a vector of all the values of an Property
        inside a context of the alert replicas associated with the alert combo.

        :param string context: the name of the context
        :param string propname: the name of the Property

        :return: a list of values
        :rtype: list
        """
        pass

class AOContext( Context ):
    """
    Represents a AO (Astro Object) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under AO context.

    :param: astro_id(int): ID of the astro object that owns the context.
    """
    name = 'AO'
    """
    Name of AO context.

    :type: string
    """

    def __init__( self, astro_id ):
        """'continer_id' is the ID of the object that owns the context."""
        self.container_id = astro_id
        self.container_type = 'A'

        ## Initialize predefined base properties for AO context.
        for propname in AO_base_properties.keys():
            prop = Property( propname, BASE_PROP, self,
                              AO_base_properties[propname][0], 1,
                              description=AO_base_properties[propname][1] )
            setattr( self, propname, prop )

        ## Connect to mysql database.
        conn = GetDBConn()
        cur = conn.cursor()
        # FIXME: not always SDSS
        row = None
        query = """select * from AstroObject_NED where No={}""".format(astro_id)
        cur.execute( query )
        row = cur.fetchall()
        if len(row) != 0:
            row = row[0]
            
        # query = """select * from AstroObject_Fake_SDSS where Objid={}""".format(astro_id)
        # cur.execute( query )
        # row = cur.fetchall()
        # if len(row) != 0:
            # row = row[0]

        # query = """select * from AstroObject_Fake_Chandra where msid={}""".format(astro_id)
        # cur.execute( query )
        # row = cur.fetchall()
        # if len(row) != 0:
            # row = row[0]

        if row is None:
            conn.close()
            return

        for propname in AO_base_properties.keys():
            prop = getattr( self, propname )
            try:
                prop.value = row[ AO_base_properties[propname][2] ]
            except:
                prop.value = None

        conn.close()

    def __str__( self ):
        buf = StringIO()
        buf.write( '{0} Context:\n'.format(self.name) )
        for propname in AO_base_properties.keys():
            prop = getattr( self, propname )
            if prop.valueAssigned == True:
                buf.write( 'Property: {0}, datatype: {1}, value: {2:.2f}\n'
                           .format(prop.name, prop.datatype, prop.value) )

        return buf.getvalue()

    ## Flush propiubtes under AR to DB if their values is not synced.
    def commit( self, cur ):
        for propname in AO_base_properties.keys():
            prop = getattr( self, propname )
            if prop.valueAssigned and prop.flushed2DB == False:
                prop.flushed2DB = True
                sql_insert = """insert into PropertyValue(ContainerID,ContainerType,Value, PropName, ComputedAt) \
                values({0},"{1}",{2},"{3}", "{4}")""".format( self.container_id,'O' , prop.value, prop.name, time.time() )
                cur.execute( sql_insert )
                #print( 'Committing {0}, flushed flag={1}'.format(prop.name, prop.flushed2DB) )


class LAContext( Context ):
    """
    Represents a LA (Locus-aggregated Alert) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under LA context.

    :param: container_id(int): ID of the object that owns the context.
    """
    name = 'LA'
    """
    Name of LA context.

    :type: string
    """

    def __init__( self, container_id ):
        """'continer_id' is the ID of the object that owns the context."""
        self.container_id = container_id
        self.conn = GetDBConn()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def assembleTimeSeries_replicas( self, context, propname ):
        """
        The function assembles a time series of all the past values
        of an Property inside a context of the alert replicas associated
        with a locus aggregated alert.

        :param string context: the name of the context
        :param string propname: the name of the Property

        :return: a time series of values. Here the value is a dict that maps
                 replica ID to the real value of ``propname``.
        :rtype: :py:class:`pandas.Series`
        """
        pass

    def assembleTimeSeries_cameraAlerts( self, context, propname, passband=None ):
        """
        The function assembles a time series of all the past values
        of an Property inside a context of the camera alerts associated
        with a locus aggregated alert.

        :param string context: the name of the context
        :param string propname: the name of the Property

        :return: a time series of values
        :rtype: an array of three element tuple: (time, value, annotation)
        """
        ## Connect to mysql database.
        cur = self.conn.cursor()

        query = """select ComputedAt, Value, Annotation from PropertyValue where ContainerID={0} and
        ContainerType="E" and PropName="{1}" """.format( self.container_id, propname )
        if propname == 'Magnitude' and passband is not None:
            query += """ and Annotation="{}" """.format(passband)
        cur.execute( query )
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append(tuple(row))

        return result

    def addProperty(self, propname, value, computed_time=time.time()):
        cur = self.conn.cursor()
        query = """ insert into PropertyValue (ContainerID,ContainerType,ComputedAt,Value,PropName) 
                    values ({},"L","{}",{},"{}")""".format(self.container_id,computed_time,value,propname)
        cur.execute(query)
        self.conn.commit()

    def assembleProperties(self, propname):
        cur = self.conn.cursor()

        query = """select ComputedAt, Value, Annotation from PropertyValue where ContainerID={0} and
        ContainerType="L" and PropName="{1}" limit 300 """.format( self.container_id, propname )

        cur.execute( query )
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append(tuple(row))

        return result

    def setScalar(self, propname, value):
        cur = self.conn.cursor()

        if propname == 'filters':
            db_value = 0
            # order: u,g,r,i,z
            if 'u' in value:
                db_value += 10000
            if 'g' in value:
                db_value += 1000
            if 'r' in value:
                db_value += 100
            if 'i' in value:
                db_value += 10
            if 'z' in value:
                db_value += 1
            value = db_value
                
        # query = """select Value from PropertyValue where ContainerID={0} and PropName="{1}" """.format(self.container_id, propname)
        # cur.execute( query )
        # results = cur.fetchall()
        # if len(results) == 0: # the Property has never been stored in DB
            # query = """ insert into PropertyValue (ContainerID,ContainerType,ComputedAt,Value,PropName) 
                        # values ({},"L","{}",{},"{}")""".format(self.container_id,time.time(),value,propname)
        # else:
            # query = """ update PropertyValue set Value={} where ContainerID={} and PropName="{}" """.format(value, self.container_id, propname)

        # query_delete = """ delete from PropertyValue where ContainerID={} and PropName="{}" """.format(self.container_id, propname)
        # cur.execute(query_delete)
        query_insert = """ insert into PropertyValue (ContainerID,ContainerType,ComputedAt,Value,PropName) 
                        values ({},"L","{}",{},"{}")""".format(self.container_id,time.time(),value,propname)
        cur.execute(query_insert)

    def getScalar(self, propname):
        cur = self.conn.cursor()

        query = """select Value from PropertyValue where ContainerID={0} and PropName="{1}" order by id DESC """.format(self.container_id, propname)
        cur.execute( query )
        results = cur.fetchall()
        if len(results) == 0:
            return None
        else:
            if propname == 'filters':
                f = ""
                db_value = int(results[0][0])
                if db_value / 10000 == 1:
                    f += 'u'
                if db_value % 10000 / 1000 == 1:
                    f += 'g'
                if db_value % 1000 / 100 == 1:
                    f += 'r'
                if db_value % 100 /10 == 1:
                    f += 'i'
                if db_value % 10 == 1:
                    f += 'z'
                
                return f

            else:
                return float(results[0][0]) # TODO cast to real type

    def DBCommit(self):
        self.conn.commit()

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
    pass

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
    pass

class ISContext( Context ):
    """
    Represents a IS (Image Section) context object which is a sub-class of :py:class:`Context`.
    It contains all the properties defined under IS context.
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
    It contains all the properties defined under IR context.
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
    It contains all the properties defined under PS context.
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
    It contains all the properties defined under ES context.
    """
    name = 'ES'
    """
    Name of ES context.

    :type: string
    """
    pass
