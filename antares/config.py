"""
Configurations for Antares project.
"""

#!/usr/bin/env python3

import numpy

## Path to the astro catalog data used for demo
demo_data_path = '../demo-data'

## Base attributes under CA context.
CA_base_attributes = {
    'RA' : (float, 'Right ascension'),
    'Decl' : (float, 'Declination'),
    'Magnitude' : (float, 'Logarithmic measure of the brightness of an alert'),
    'MagnitudeErr' : (float, 'Error of magnitude of an alert'),
}

## Derived attributes under CA context.
CA_derived_attributes = {
    'P' : (float, 'Best fit period'),
    'A' : (float, 'Light curve amplitude'),
    'mmed' : (float, 'Median LINEAR magnitude'),
    'stdev' : (float, 'standard deviation of LINEAR magnitudes'),
    'kurt' : (float, 'kurtosis in LINEAR light curves'),
    #'skew' : (float, 'skewness in LINEAR light curves'),
}

BASE_ATTR = 0     # indicate base attribute
DERIVED_ATTR = 1  # indicate derived attribute

## We can generate upto this many camera alerts for the demo.
total_num_alerts = 7194
