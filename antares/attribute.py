#!/usr/bin/env python3
    
class Attribute:
    """
    Represents an attribute object. An attribute is initialized with its name,
    the context it belongs to, the datatype of its value, a description and the scale of its value.

    :param: name(string): name of the attribute
    :param: context(:py:class:`antares.context.Context`): context the attribute belongs to
    :param: datatype(string): data type of the attribute value
    :param: scale(:py:class:`IntPair`): the range to which the attribute value scales
    :param: description(string): description of the attribute
    """

    vector = None
    """
    The vector of all the past values computed for the attribute.
    It is a Numpy array.

    :type: numpy array
    """

    time_series = None
    """
    The time series of all the past values computed for the attribute.
    It is a Pandas Time Series.

    :type: pandas series
    """

    description = ""
    """
    A short description of the attribute.

    :type: string
    """

    name = ""
    """
    The name of the attribute.

    :type: string
    """

    context = ""
    """
    The context that the attribute belongs to.

    :type: string
    """

    datatype = ""
    """
    The data type of the attribute. The valid data type could be either
    a Python's built-in type (boolean, int, float, string, timestamp) or a composite
    object (UncertainFloat, ProbabilityCurve, IntPair, FloatPair, TimePeriod).

    :type: string
    """

    timestamp = None
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
    A finite list of possible int values for the attribute. It is
    available only when datatype = "enumerated int". In that case the
    attribute value can be only picked from this list.

    :type: list of ints
    """

    enum_strs = None
    """
    A finite list of possible string values for the attribute. It is
    available only when datatype = "enumerated string". In that case the
    attribute value can be only picked from this list.

    :type: list of strings
    """

    def __init__( self, name, context, datatype, scale, description="" ):
        pass

    def timeDelimitedSeries( self, start_time, end_time ):
        """
        A time-delimited series of all the past values of the attribute.

        :param timestamp start_time: the start of time series
        :param timestamp end_time: the end of time series

        :return: time series of the attribute values from `start_time` to
                  `end_time`.
        :rtype: Pandas Time Series
        """
        pass

class UncertainFloat:
    """Represents a triple floats which is one of the data type of
    :py:class:`antares.attribute.Attribute`. It consists of three float values, one being the expected
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
    """Represents a probability curve which is one of the data type of
    :py:class:`Attribute`. It is used for variability."""
    probabilities = None
    """
    A list of probability values.

    :type: numpy array
    """
    
class IntPair:
    """Represents a pair of int (providing lower and upper bounds)
    which is one of the data type of :py:class:`Attribute`."""
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
    which is one of the data type of :py:class:`Attribute`."""
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
    """A derived attribute of the existence time for the
    locus-aggregated alert. It is a data type of :py:class:`Attribute`."""
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
