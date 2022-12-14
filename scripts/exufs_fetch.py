# =========================================================================

# Script: scripts/exufs_fetch.py

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
Script
------

    exufs_fetch.py

Description
-----------

    This script contains a functional application interface to collect
    (i.e., fetch) file paths specified within a YAML-formatted
    application file.

Functions
---------

    main()

        This is the driver-level method to invoke the tasks within
        this script.

Author(s)
---------

    Henry R. Winterbottom; 12 December 2022

History
-------

    2022-12-12: Henry Winterbottom -- Initial implementation.

"""

# ----

import os
import time

from staging.fetch import Fetch
from utils.arguments_interface import Arguments
from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

logger = Logger()

# ----


def main():
    """
    Description
    -----------

    This is the driver-level function to invoke the tasks within this
    script.

    """

    # Collect the command line arguments.
    script_name = os.path.basename(__file__)
    start_time = time.time()
    msg = f"Beginning application {script_name}."
    logger.info(msg=msg)
    options_obj = Arguments().run()

    # Launch the task.
    task = Fetch(options_obj=options_obj)
    task.run()
    stop_time = time.time()
    msg = f"Completed application {script_name}."
    logger.info(msg=msg)
    total_time = stop_time - start_time
    msg = f"Total Elapsed Time: {total_time} seconds."
    logger.info(msg=msg)


# ----


if __name__ == "__main__":
    main()
