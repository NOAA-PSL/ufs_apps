# =========================================================================

# Script: scripts/exufs_gdas.py

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

    exufs_gdas.py

Description
-----------

    This script contains a functional application interface to the
    Global Data Assimilation System (GDAS) supported applications.

Functions
---------

    main()

        This is the driver-level method to invoke the tasks within
        this script.

Usage
-----

    user@host:$ python exufs_fetch.py <--yaml_file> <--cycle> --<work_path> \
                    --<expt_name> [--platform] [--fetch_type] [--fileid]

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
import time

from gdas import GDAS
from schema import Or
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

    expt_name: str

        A Python string specifying an (unique) name for the respective
        experiment.

    work_path: str

        A Python string specifying the path to where the experiment
        directory trees will be built and the respective experiment
        will be executed.

    app: str

        A Python string specifying the supported data assimilation
        application (i.e., GSI, SOCA, etc.,).

    app_type: str

        A Python string specifying the supported data assimilation
        application type (i.e., global_3dvar, regional_enkf, etc.,).

    """

    # Define the schema attributes.
    cls_schema = {
        "yaml_file": str,
        "cycle": Or(str, int),
        "work_path": str,
        "expt_name": str,
        "app": str,
        "app_type": str
    }

    # Collect the command line arguments.
    script_name = os.path.basename(__file__)
    start_time = time.time()
    msg = f"Beginning application {script_name}."
    Logger().info(msg=msg)
    options_obj = Arguments().run(eval_schema=True, cls_schema=cls_schema)

    # Launch the task.
    task = GDAS(options_obj=options_obj)
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
