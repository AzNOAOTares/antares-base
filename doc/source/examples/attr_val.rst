***************************************
Examples of using API
***************************************

How to assign/retrieve the value to/from an attribute
=====================================================

Suppose we have a camera alert with some base attributes, for example,
its **G** value and **R** value, if want to compute the derived
attribute **GMinusR**, we can do::

  from antares.alert import CameraAlert

  def computeGMinusR( alert ):
      """ alert """
      alert.CA.GMinusR = alert.CA.G - alert.CA.R
      alert.CA.GMinusR.confidence = 1.0
      alert.CA.GMinusR.annotation = "High confidence because we don't know"
      alert.CA.GMinusR.description = "G value minus R value"
		
