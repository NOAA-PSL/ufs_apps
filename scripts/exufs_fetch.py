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

Usage
-----

    user@host:$ python exufs_fetch.py --<yaml_file> --<cycle> --<work_path> \
                    --<expt_name> [--platform] [--fetch_type] [--fileid]

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

        --yaml_file /path/to/yaml/file or -yaml_file /path/to/yaml/file

    cycle: str

        A Python string specifying the respective forecast cycle; this
        string must be formatted as %Y%m%d%H%M%S assuming the POSIX
        convention; enter the parameter value as follows for a
        forecast cycle beginning 0000 UTC 01 January 2000:

        --cycle 20000101000000 or -cycle 20000101000000

    expt_name: str

        A Python string specifying an (unique) name for the respective
        experiment; for an experiment named SPAM, enter the parameter
        value as follows.

        --expt_name SPAM or -expt_name SPAM

    work_path: str

        A Python string specifying the path to where the experiment
        directory trees will be built and the respective experiment
        will be executed; enter the parameter value as follows.

        --work_path /path/for/spam/experiment or -work_path /path/for/spam/experiment

    Keywords
    --------

    platform: str, optional

        A Python string specifying the supported interface/platform
        types from which files are to be fetched; this argument may
        also contain a comma-delimited string for multiple supported
        interface/platform options (no spaces between comma-delimited
        values).

        For files to be fetched from the "spam" platform, the keyword
        value may be entered as:

        --platform spam or -platform spam

        For files to be fetched from both the "spam" and the "ham"
        platforms, the keyword value may be entered as:

        --platform spam,ham or -platform spam,ham

    fetch_type: str, optional

        A Python string specifying the file types to be collected; an
        example is as follows:

        fetch:

            interface:

                spam:

                ham:

        if fetch_type is specified as "spam", all files for the
        respective interface (i.e., AWS s3, NOAA HPSS, etc.,) beneath
        the "spam" block will be collected; if the keyword is not
        specified or NoneType upon entry, the attributes beneath both
        "spam" and "ham" will be returned.

        For the "spam" example above, the keyword value may be entered
        as:

        --fetch_type spam or -fetch_type spam

    fileid: str, optional

        A Python string specifying the file identifiers to be
        collected; this argument may also contain a comma-delimited
        string for multiple file identifiers (no spaces between
        comma-delimited values); if not specified, all file
        identifiers (or as a function of fetch_type above) within the
        experiment configuration will be collected; example is as
        follows:

        fetch:

            interface:

                spam:

                    ham:

                    eggs:

        The "ham" and "eggs" attributes are the file identifiers
        within the configuration file and may be used to retrieve
        specific (a) file(s). For a respective file identifier, "ham"
        for example, to be collected, the keyword value may be entered
        as:

        --fileid ham or -fileid ham

        For multiple file identifiers to be collect, "ham" and "eggs"
        in this example, the keyword value may be entered as (no
        spaces between comma-delimited values):

        --fileid ham,eggs or -fileid ham,eggs


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

from schema import Optional, Or
from staging.fetch import Fetch
from utils.arguments_interface import Arguments
from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Specify whether to evaluate the format for the respective parameter
# values.
EVAL_SCHEMA = True

# Define the schema attributes.
cls_schema = {
    "yaml_file": str,
    "cycle": Or(str, int),
    "work_path": str,
    "expt_name": str,
    Optional("fetch_type"): Or(str, None),
    Optional("platform"): Or(str, None),
    Optional("fileid"): Or(str, None),
}

# ----


def main() -> None:
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
    Logger().info(msg=msg)
    options_obj = Arguments().run(eval_schema=EVAL_SCHEMA, cls_schema=cls_schema)

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
