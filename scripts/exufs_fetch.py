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

# pylint: disable=no-name-in-module

# ----

import os
from schema import Optional, Or
import time

from staging.fetch import Fetch
from utils.arguments_interface import Arguments
from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def main() -> None:
    """
    Description
    -----------

    This is the driver-level function to invoke the tasks within this
    script.

    Parameters
    ----------

    yaml_file: str

        A Python string specifying the path to the YAML-formatted
        configuration file; this script and it's child modules assume
        that the fetch key is specified within the top-level YAML keys
        of the respective file as follows:

        fetch:

            some_stuff:

                some_more_stuff:

        Enter the parameter value as:

        --yaml_file=/path/to/yaml/file or -yaml_file=/path/to/yaml/file

    cycle: str

        A Python string specifying the respective forecast cycle; this
        string must be formatted as %Y%m%d%H%M%S assuming the POSIX
        convention; enter the parameter value as follows for a
        forecast cycle beginning 0000 UTC 01 January 2000:

        --cycle=20000101000000 or -cycle=20000101000000

    Keywords
    --------

    fetch_type: str

        A Python string specifying the file types to be collected; an
        example is as follows:

        fetch:

            interface:

                foo:

                bar:

                ocean_stuff:

        if fetch_type is specified as 'foo', all files for the
        respective interface (i.e., AWS s3, NOAA HPSS, etc.,) beneath
        the ocean_stuff block will be collected; if the keyword is not
        specified or NoneType upon entry, the attributes beneath both
        'foo' and 'bar' will be returned.

        For the 'foo' example above, the keyword value may be entered
        as:

        --fetch_type=foo or -fetch_type=foo

    """

    # Define the schema attributes.
    cls_schema = {'yaml_file': str,
                  'cycle': Or(str, int),
                  Optional('fetch_type'): str,
                  Optional('platform_opt'): str,
                  Optional('fileid_opt'): str
                  }

    # Collect the command line arguments.
    script_name = os.path.basename(__file__)
    start_time = time.time()
    msg = f"Beginning application {script_name}."
    Logger().info(msg=msg)
    options_obj = Arguments().run(eval_schema=True, cls_schema=cls_schema)

    # Launch the task.
    task = Fetch(options_obj=options_obj)
    task.run()
    stop_time = time.time()
    msg = f"Completed application {script_name}."
    Logger().info(msg=msg)
    total_time = stop_time - start_time
    msg = f"Total Elapsed Time: {total_time} seconds."
    Logger().info(msg=msg)


# ----


if __name__ == "__main__":
    main()
