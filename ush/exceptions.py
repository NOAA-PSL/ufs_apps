# =========================================================================

# Module: ush/exceptions.py

# Author: Henry R. Winterbottom

# Email: henry.winterbottom@noaa.gov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the respective public license published by the
# Free Software Foundation and included with the repository within
# which this application is contained.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# =========================================================================

"""
Module
------

    exceptions.py

Description
-----------

    This module loads the exceptions package.

Classes
-------

    GDASError()

        This is the base-class for exceptions encountered within the
        ush/gdas module; it is a sub-class of Error.

    LaunchError()

        This is the base-class for exceptions encountered within the
        ush/launch module; it is a sub-class of Error.

    SOCAError()

        This is the base-class for exceptions encountered within the
        ush/gdas/soca module; it is a sub-class of Error.

    StagingError()

        This is the base-class for exceptions encountered within the
        ush/staging module; it is a sub-class of Error.


Author(s)
---------

    Henry R. Winterbottom; 29 December 2022

History
-------

    2022-12-29: Henry Winterbottom -- Initial implementation.

"""

# ----

from utils.error_interface import Error

# ----

# Define all available attributes.
__all__ = [
    "GDASError",
    "LaunchError",
    "SOCAError",
    "StagingError",
]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class GDASError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/gdas module; it is a sub-class of Error.

    """

# ----


class LaunchError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/launch module; it is a sub-class of Error.

    """

# ----


class SOCAError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/gdas/soca module; it is a sub-class of Error.

    """

# ----


class StagingError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/staging module; it is a sub-class of Error.

    """
