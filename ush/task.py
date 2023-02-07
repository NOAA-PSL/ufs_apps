# =========================================================================

# Module: ush/task.py

# Author: Rahul Mahajan and Henry R. Winterbottom

# Email: rahul.mahajan@noaa.gov and henry.winterbottom@noaa.gov

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

    task.py

Description
-----------

    This module contains the base-class object for all tasks.

Classes
-------

    Task(options_obj, *args, **kwargs)

        This is the base-class object for all tasks.

Notes
-----

    This implementation is based on and expanded upon the module found
    at https://tinyurl.com/pygw-task-module.

Requirements
------------

- ufs_pyutils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 06 February 2023

History
-------

    2023-02-06: Henry Winterbottom -- Initial implementation.

"""

# ----

from dataclasses import dataclass
from typing import Dict, Tuple

from confs.yaml_interface import YAML
from tools import datetime_interface, fileio_interface, parser_interface
from utils import timestamp_interface
from utils.logger_interface import Logger

from exceptions import TaskError

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


@dataclass
class Task:
    """
    Description
    -----------

    This is the base-class object for all tasks.

    Parameters
    ----------

    options_obj: object

        A Python object containing the attributes collect via the
        command line from the application driver script.

    args: tuple

        A Python tuple containing additional arguments passed from the
        sub-class constructor.

    Keywords
    --------

    kwargs: dict, optional

        A Python dictionary containing keyword arguments from the
        sub-class constructor.

    Raises
    ------

    TaskError:

        * raised if the path to the YAML-formatted configuration file,
          passed via the commmand line options object (options_opt),
          cannot be located using the specified path.

        * raised if the run-time environment does not contain a
          mandatory environment variable.

    """

    def __init__(self, options_obj: object, *args: Tuple, **kwargs: Dict):
        """
        Description
        -----------

        Creates a new Task object.

        """

        # Define the base-class attributes.
        self.options_obj = options_obj
        self.logger = Logger()

        # Collect the experiment attributes from the experiment
        # configuration file; proceed accordingly.
        if not fileio_interface.fileexist(path=self.options_obj.yaml_file):
            msg = (
                f"The YAML-formatted experiment configuration file {self.options_obj.yaml_file} "
                "does not exist. Aborting!!!"
            )
            raise TaskError(msg=msg)

        self.config_obj = YAML().read_yaml(
            yaml_file=self.options_obj.yaml_file, return_obj=True
        )

        # Collect the arguments specified upon entry and update the
        # base-class object.
        for arg in args:
            self.config_obj = parser_interface.object_setattr(
                object_in=self.config_obj, key=str(arg), value=args[arg]
            )

        # Collect the keyword arguments specified upon entry and
        # update the base-class object.
        for (kwarg, value) in kwargs.items():
            self.config_obj = parser_interface.object_setattr(
                object_in=self.config_obj, key=kwarg, value=value
            )

        # Check that the mandatory variables for the experiment are
        # found in the configuration file.

        # COMMENT: Leaving CDUMP for now and will remove when
        # instructed.

        # Define the mandatory run time keys for the respective
        # experiment cycle; proceed accordingly.
        # "CDUMP", "DATA", "PDY", "RUN", "cyc"]
        mand_attr_list = ["PDY", "cyc"]
        for mand_attr in mand_attr_list:

            value = parser_interface.enviro_get(envvar=mand_attr)

            if value is None:
                msg = (
                    f"The mandatory key {mand_attr} could not be determined "
                    "from the runtime environment. Aborting!!!"
                )
                raise TaskError(msg=msg)

            self.config_obj = parser_interface.object_setattr(
                object_in=self.config_obj, key=mand_attr, value=value
            )

        # Check that the mandatory run time keys are formatted
        # accordingly.
        self.__check_mand_attrs__()

        # Define the relevant forecast cycles accordingly.
        self.__define_cycle_timestamps__()

    def __check_mand_attrs__(self) -> None:
        """
        Description
        -----------

        This method checks that the mandatory argument assigned values
        are formatted correctly.

        Raises
        ------

        TaskError:

            * raised if an exception is encounterd while checking the
              respective attribute format.

        """

        # Define a Python dictionary containing the format for the
        # respective mandatory attributes.
        mand_attr_dict = {
            "PDY": "%Y%m%d",
            "cyc": "%H",
        }

        for (mand_attr, mand_attr_value) in mand_attr_dict.items():

            # Check that the respective timestamp string is of the
            # expected format; proceed accordingly.
            try:
                timestamp_interface.check_frmt(
                    datestr=parser_interface.object_getattr(
                        object_in=self.config_obj, key=mand_attr
                    ),
                    in_frmttyp=mand_attr_value,
                    out_frmttyp=mand_attr_value,
                )

            except Exception as errmsg:

                msg = (
                    f"Validating the format for runtime variable {mand_attr} "
                    f"failed with error {errmsg}. Aborting!!!"
                )
                raise TaskError(msg=msg) from errmsg

    def __define_cycle_timestamps__(self) -> None:
        """
        Description
        -----------

        This method will define the previous and subsequent forecast
        cycle times if the experiment configuration contains the
        attributes cycling and cycling_interval_seconds and defined
        appropriately; if the cycling option has not been specified
        the respective previous and subsequent forecast cycle times
        are not specified.

        Raises
        ------

        TaskError:

            * raise if an AttributeError exception is encountered;
              this typically implies that the experiment configuration
              has specified a cycling application but has not provided
              a cycling interval (see cycling_interval_seconds).

        """

        # Check whether the respective experiment configuration
        # permits cycling; proceed accordingly.
        cycling = parser_interface.object_getattr(
            object_in=self.config_obj, key="cycling", force=True
        )
        if cycling is None:

            msg = (
                f"The experiment configuration found in {self.options_obj.yaml_file} "
                "does not specify the configurtion attribute cycling and therefore "
                "cycling will not be supported."
            )
            self.logger.warn(msg=msg)

            return

        try:
            if (
                cycling is not None
                and cycling
                and self.config_obj.cycling_interval_seconds
            ):
                pass

        except AttributeError as exc:

            msg = (
                "For cycling experiment applications the configuration variable "
                "cycling_interval_seconds must be specified in file "
                f"{self.options_obj.yaml_file}. Aborting!!!"
            )
            raise TaskError(msg=msg) from exc

        # Define the timestamps for the previous and subsequent
        # cycles.
        ptime = datetime_interface.datestrupdate(
            datestr=self.config_obj.cycle,
            in_frmttyp=timestamp_interface.GLOBAL,
            out_frmttyp=timestamp_interface.GLOBAL,
            offset_seconds=int(-1 * self.config_obj.cycling_interval_seconds),
        )
        self.config_obj = parser_interface.object_setattr(
            object_in=self.config_obj, key="ptime", value=str(ptime)
        )

        ntime = datetime_interface.datestrupdate(
            datestr=self.config_obj.cycle,
            in_frmttyp=timestamp_interface.GLOBAL,
            out_frmttyp=timestamp_interface.GLOBAL,
            offset_seconds=self.config_obj.cycling_interval_seconds,
        )
        self.config_obj = parser_interface.object_setattr(
            object_in=self.config_obj, key="ntime", value=str(ntime)
        )

    def initialize(self) -> None:
        """
        Description
        -----------

        This method is generic and used to initialize the respective
        calling class (i.e., Task sub-class) applications; it may be
        overloaded by the respective calling class methods.

        """

    def execute(self) -> None:
        """
        Description
        -----------

        This method is generic and used to execute the methods for the
        respective calling class (i.e., Task sub-class) applications.

        """

    def finalize(self):
        """
        Description
        -----------

        This method is generic and used to finalize the calling
        application (i.e., Task sub-class).

        """
