from antares.config import *
import numpy as np
import pymysql
from datetime import datetime

class Property:
    """
    This is the Property class. A property is initialized with its name,
    the context it belongs to, the datatype of its value, a scale, and the description of its value.

    :param: name(string): name of the property
    :param: context(:py:class:`antares.context.Context`): context the property belongs to
    :param: datatype(string): data type of the property value
    :param: scale(:py:class:`IntPair` or :py:class:`FloatPair`): the range to which the property value scales
    :param: scale(:py:class:`FloatPair`): the range to which the property value scales
    :param: description(string): description of the property
    """

    vector = None
    """
    The vector of all the past values computed for the property.
    It is a Numpy array.

    :type: numpy array
    """

    description = ""
    """
    A short description of the property.

    :type: string
    """

    name = ""
    """
    The name of the property.

    :type: string
    """

    context = ""
    """
    The context that the property belongs to.

    :type: string
    """

    datatype = ""
    """
    The data type of the property. The valid data type could be one of the following:
    (1) a Python's built-in primitive type ("boolean", "int", "float", "string"), (2) a Python package
    ("timestamp"), or (3) a proprietary, composite object provided by ANTARES
    (:py:class:`antares.context.UncertainFloat`, :py:class:`antares.context.ProbabilityCurve`,
    :py:class:`antares.context.IntPair`, :py:class:`antares.context.FloatPair`, :py:class:`antares.context.TimePeriod`)
    as are documented within the API.

    :type: string
    """

    computedAt = None
    """
    Time stamp for the most-recently computed value.

    :type: timestamp
    """

    annotation = ""
    """
    Annotation for the most-recently computed value.

    :type: string
    """

    confidence = 1.0
    """
    Confidence for the most-recently computed value.

    :type: float
    """

    enum_ints = None
    """
    A finite list of possible int values for the property. It is
    available only when datatype = "enumerated int". In that case the
    property value can be only picked from this list.

    :type: list of ints
    """

    def __init__( self, name, atype, context, datatype, scale, description="" ):
        self.name = name
        self.atype = atype
        self.context = context
        self.datatype = datatype
        self.scale = scale
        self.description = description
        self.valueAssigned = False
        self.history = [] # List of (computeAt, value) tuples
        self.flushed2DB = False
        self.loaded = False

    def get_value( self ):
        if self.valueAssigned == True:
            return self._value

        if self.loaded == False:
            ## Query the DB to see if the value for the property has already been computed.
            conn = GetDBConn()
            cursor = conn.cursor()
            query = """select Value from PropertyValue where ContainerID={0} \
            and ContainerType="{1}" and PropName="{2}" """.format( self.context.container_id,
                                                                   self.context.container_type,
                                                                   self.name )
            cursor.execute( query )
            rows = cursor.fetchall()
            if len(rows) == 1:
                self.loaded = True
                if rows[0][0] == None:
                    return None
                self._value = self.datatype( rows[0][0] )
                #print( 'Value for {0} of alert {1} has been computed as {2}!'.
                #       format( self.name, self.context.container_id, self._value ) )

        if hasprop( self, '_value' ):
            return self._value
        else:
            return None
            #raise PropertyError( 'Value for {0} has not been set!'.format(self.name) )

    def set_value( self, val ):
        ## Check if 'val' is of the desired type.
        if not isinstance( val, self.datatype ):
            try:
                val = self.datatype( val )
            except ValueError:
                raise TypeError( '{0} should be a {1}!'.format(val, self.datatype) )

        self._value = val
        self.valueAssigned = True
        if self.atype == DERIVED_PROP:
            # Set timestamp of computation.
            self.computedAt = datetime.now().timestamp()
            self.history.append( (self.computedAt, self._value ) )
            # Indicate the value of derived property has not been written
            # to DB yet. When alert.commit() is called, this flag will become True.
            self.flushed2DB = False

    def get_confidence( self ):
        if hasprop( self, '_confidence' ):
            return self._confidence
        else:
            return None

    def set_confidence( self, confid ):
        ## Check if 'val' is of the desired type.
        if isinstance( confid, float ) or isinstance( confid, int ):
            self._confidence = confid
        else:
            raise TypeError( '{0} should be a {1}!'.format(confid, float) )

    def get_annotation( self ):
        if hasprop( self, '_annotation' ):
            return self._annotation
        else:
            return ''

    def set_annotation( self, annotation ):
        ## Check if 'val' is of the desired type.
        if not isinstance( annotation, str ):
            raise TypeError( '{0} should be a {1}!'.format(confid, str) )

        self._annotation = annotation

    ## Attach getters & setters
    value = property( get_value, set_value )
    confidence = property( get_confidence, set_confidence )
    annotation = property( get_annotation, set_annotation )

class UncertainFloat:
    """Represents a triple floats which is one of the data types available to
    :py:class:`antares.property.Property`. It consists of three float values, one being the expected
    value, a second being the lower std dev (one std dev below) and the
    third being the upper std dev (one std dev above)."""
    expected_value = None
    """
    The first float: expected value.

    :type: float
    """

    lower_stddev = None
    """
    The second float: lower std dev (one std dev below).

    :type: float
    """

    upper_stddev = None
    """
    The third float: upper std dev (one std dev above).

    :type: float
    """

class ProbabilityCurve:
    """Represents a probability curve which is one of the data types available to
    :py:class:`Property`. It is used to encapsulate numerical values which have statistical certainty."""
    probabilities = None
    """
    A set of variables which include the estimated value (any of the types available to Property) and
    statistical measures (floats) describing the certainty of that value.  The exact nature of the statistical
    measures depends on data type and desired statistical model, but generally include (for a numerical value)
    mean, median, Q1, Q3, and standard deviation.  This type will be developed as it is used and more
    statistical models are needed.

    :type: numpy array
    """

class IntPair:
    """Represents a pair of int (providing lower and upper bounds)
    which is one of the data types available to :py:class:`Property`."""
    lower_bound = None
    """
    The value of lower bound.

    :type: int
    """

    upper_bound = None
    """
    The value of upper bound.

    :type: int
    """

class FloatPair:
    """Represents a pair of float (providing lower and upper bounds)
    which is one of the data types available to :py:class:`Property`."""
    lower_bound = None
    """
    The value of lower bound.

    :type: float
    """

    upper_bound = None
    """
    The value of upper bound.

    :type: float
    """

class TimePeriod:
    """A derived property of the existence time for the
    locus-aggregated alert. It is a data type available to :py:class:`Property`."""
    start = None
    """
    The start of the time period.

    :type: timestamp
    """

    end = None
    """
    The end of the time period.

    :type: timestamp
    """


