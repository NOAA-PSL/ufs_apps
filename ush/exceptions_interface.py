# =========================================================================

# Module: ush/exceptions_interface.py

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

    exceptions_interface.py

Description
-----------

    This module loads the exceptions package.

Classes
-------

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
    "StagingError",
]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class StagingError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ush/staging module; it is a sub-class of Error.

    """
