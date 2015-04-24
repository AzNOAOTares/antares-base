"""
Configurations for Antares project.
"""

#!/usr/bin/env python3

from antares.attribute import *
import numpy

## Path to the astro catalog data used for demo
demo_data_path = '../demo-data'

## Base attributes under CA context.
CA_attributes = { 'RA' : (numpy.float64, 'Right ascension'),
                  'Decl' : (numpy.float64, 'Declination'),
                  'LCtype' : (numpy.int64, 'Type of light curve'),
                  'P' : (numpy.float64, 'Best fit period'),
                  'A' : (numpy.float64, 'Light curve amplitude'),
                  'Mmed' : (numpy.float64, 'Median LINEAR magnitude'),
                  'Stdev' : (numpy.float64, 'standard deviation of LINEAR magnitudes'),
                  'Rms' : (numpy.float64, 'robust estimate of the standard deviation based on interquartile range'),
                  'Lchi2pdf' : (numpy.float64, 'base 10 logarithm of the chi2 per degree of freedom computed assuming no variation'),
                  'NObs' : (numpy.float64, 'number of LINEAR observations'),
                  'Skew' : (numpy.float64, 'skewness in LINEAR light curves'),
                  'Kurt' : (numpy.float64, 'kurtosis in LINEAR light curves'),
                  'CUF' : (numpy.int64, 'classification uncertainty flag'),
                  'G' : (numpy.float64, 'Brightness(magnitude) generated by G-filter'),
                  'R' : (numpy.float64, 'Brightness(magnitude) generated by R-filter') }

## We can generate upto this many camera alerts for the demo.
total_num_alerts = 7194
