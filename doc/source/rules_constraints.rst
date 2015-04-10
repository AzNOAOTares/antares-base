.. Antares API documentation master file, created by
   sphinx-quickstart on Tue Mar 10 20:02:16 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*************************************************
Rules & Constraints
*************************************************

1. Attributes can be only accessed through the context that they belong to.

2. Values of Attributes are accessed directly by their names.
   For example:

   >>> value = alert.CA.GMinusR

   This will assign most-recently computed value for the attribute GMinusR
   to ``value``. It will raise an :py:exc:`AttributeError` exception if CA context
   has no attribute called ``GMinusR``.

3. Attributes are changed when we assign values to them.
   For example:

   >>> alert.CA.GMinusR = value

   This will assign ``value`` to the attribute ``GMinusR`` that is defined under
   CA context. It will raise an :py:exc:`AttributeError` exception if CA context
   has no attribute called ``GMinusR``.

4. Timestamp for a newly computed attribute value is assigned implicitly
   when the value is assigned to the attribute.

5. Exceptions are handled by callers. The only exception in the API is Python's
   built-in :py:exc:`AttributeError` exception.

6. There will be a max size for strings. The max size is to be determined.

7. The value of an attribute may be NA (not applicable), but NK (not known)
   is not allowed as a value.
