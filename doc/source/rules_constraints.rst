.. Antares API documentation master file, created by
   sphinx-quickstart on Tue Mar 10 20:02:16 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*************************************************
Rules & Constraints
*************************************************

1. Properties can be only accessed through the context that they belong to.

2. Values of Properties are accessed directly by their names.
   For example:

   >>> value = alert.CA.GMinusR

   This will assign most-recently computed value for the property GMinusR
   to ``value``. It will raise an :py:exc:`AttributeError` exception if CA context
   has no property called ``GMinusR``.

3. Properties are changed when we assign values to them.
   For example:

   >>> alert.CA.GMinusR = value

   This will assign ``value`` to the property ``GMinusR`` that is defined under
   CA context. It will raise an :py:exc:`AttributeError` exception if CA context
   has no property called ``GMinusR``.

4. Timestamp for a newly computed property value is assigned implicitly
   when the value is assigned to the property.

5. Exceptions are handled by callers. The only exception in the API is Python's
   built-in :py:exc:`AttributeError` exception.

6. There will be a max size for strings. The max size is to be determined.

7. The value of an property may be NA (not applicable), but NK (not known)
   is not allowed as a value.

8. The value for a Base Property is provided by the Camera in a
   camera alert or from the Aggregated AstroObject Catalogue for the
   relevant alert replica, and is always present when appropriate.

9. The value for a Derived Property will be present for a derivation
   function for a given context if its arguments are present and if
   the algorithm for that derivation function completes.

10. CA and LA properties are always available.

11. AR properties are only accessible during per-replica processing;
    AO properties are available if ``AR-HasAstroObject`` is
    :py:data:`True`; ES only if ``AO-kind = "extended source"``; PS only if
    ``AR-HasAstroObject`` is :py:data:`True` and ``AO-kind = "point
    source"``. 

12. CB properties are only visible during per-combo processing.

13. CA processing can iterate through the alerts of its
    locus-aggregated alert to access AR, PS, and ES properties. For
    example: 

    >>> alert.LA.assembleTimeSeries_replics( 'AR', 'Redshift' )

    Here, ``alert`` is a camera alert and the above call returns a
    time series of all the values of the property ``Redshift`` under
    ``AR`` context of the alert replicas associated with a locus
    aggregated alert.

14. CB processing can iterate through its replicas to access AR, AO,
    PS, and ES properties.

    >>> combo.CB.assembleVector( 'AR', 'Redshift' )

    Here, ``combo`` is an alert combo and the above call returns a
    numpy array of all the values of the property ``Redshift`` under
    ``AR`` context of the alert replicas associated with the alert
    combo.

15. A derived property cannot have a circular definition (and so
    definitions form a directed acyclic graph).

