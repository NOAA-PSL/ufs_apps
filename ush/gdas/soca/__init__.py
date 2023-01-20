# =========================================================================

# Module: ush/gdas/soca/__init__.py

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

PLACE HOLDER

"""

# ----

# pylint: disable=line-too-long
# pylint: disable=unused-argument

# ----


# ----

import os

from dataclasses import dataclass

from confs.yaml_interface import YAML
from exceptions import SOCAError
from launch import Launch
from tools import datetime_interface, fileio_interface, parser_interface
from utils import timestamp_interface
from utils.error_interface import msg_except_handle
from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


@dataclass
class SOCA:
    """

    PLACE HOLDER

    """

    def __init__(self, options_obj: object, task_id: str):
        """
        Description
        -----------

        Creates a new SOCA object.

        """

        # Define the base-class attributes.
        self.options_obj = options_obj
        self.launch = Launch(options_obj=self.options_obj, task_id=task_id)
        self.expt_path = self.launch.build_dirpath()
        self.launch.build_configs()

        # Parse the YAML-formatted file and build the working
        # directory; proceed accordingly.
        self.yaml_dict = YAML().read_concat_yaml(yaml_file=self.options_obj.yaml_file)

    def build_dirtree(self, dirpath: str, is_ens: bool = False) -> None:
        """
        Description
        -----------

        This method builds the sub-directory tree beneath the
        top-level directory path (specified upon entry) in accordance
        with the SOCA application attributes.

        Parameters
        ----------

        dirpath: str

            A Python string specifying the top-level directory path
            beneath which the sub-directory tree will be built.

        Keywords
        --------

        is_ens: bool, optional

            A Python boolean valued variable specifying whether the
            sub-directory tree for an SOCA ensemble-based application
            is to be built.

        """

        # Define the list of sub-directories to be created; proceed
        # accordingly.
        subdirs_list = ["ANALYSIS", "bump", "INPUT", "obs", "OUTPUT",
                        "RESTART", "RESTART_IN"]

        # If working within ensemble based SOCA applications, proceed
        # accordingly.
        if is_ens:
            subdirs_list = [subdirs_list.append(subdir) for subdir in ["ensemble", "letkf_observer_obs", "letkf_solver_obs",
                                                                       "update"]]

        # Build the directory tree path(s).
        for subdir in subdirs_list:
            path = os.path.join(dirpath, subdir)
            fileio_interface.dirpath_tree(path=path)

# ----


@msg_except_handle(SOCAError)
def error(msg: str) -> None:
    """
    Description
    -----------

    This function is the exception handler for the respective module.

    Parameters
    ----------

    msg: str

        A Python string containing a message to accompany the
        exception.

    """
