# =========================================================================

# Module: ush/launch.py

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

"""

# ----

import os

from confs.yaml_interface import YAML
from tools import fileio_interface
from tools import parser_interface
from utils import timestamp_interface
from utils.error_interface import Error
from utils.logger_interface import Logger

# ----


class Launch:
    """

    """

    @classmethod
    def __init__(cls, options_obj: object):
        """
        Description
        -----------

        Creates a new Launch object.

        """

        # Define the base-class attributes.
        self = cls
        self.options_obj = options_obj
        self.logger = Logger()

        # Check that the mandatory arguments have been provided within
        # the options_obj parameter; proceed accordingly.
        mand_args_list = ["cycle", "expt_name", "work_path", "yaml_file"]

        for mand_arg in mand_args_list:

            # Check that the mandatory argument has been provided;
            # proceed accordingly.
            value = parser_interface.object_getattr(
                object_in=self.options_obj, key=mand_arg, force=True
            )

            if value is None:
                msg = (
                    "The option attributes provided to the base-class does not "
                    f"contain the mandatory attribute {mand_arg}. Aborting!!!"
                )
                raise LaunchError(msg=msg)

            # Update the base-class object attribute.
            self = parser_interface.object_setattr(
                object_in=self, key=mand_arg, value=value
            )

        # Check that the timestamp string is of the correct format;
        # proceed accordingly.
        timestamp_interface.check_frmt(
            datestr=self.cycle,
            in_frmttyp=timestamp_interface.GLOBAL,
            out_frmttyp=timestamp_interface.GLOBAL,
        )

        # Check that the YAML-formatted configuration file exists;
        # proceed accordingly.
        exist = fileio_interface.fileexist(path=self.yaml_file)

        if not exist:
            msg = (
                f"The YAML-formatted configuration file {self.yaml_file} "
                "does not exist. Aborting!!!"
            )
            raise LaunchError(msg=msg)

        # Parse the configuration file.
        self.yaml_dict = fileio_interface.read_yaml(yaml_file=self.yaml_file)

    def build_config(self) -> None:
        """ """

        yaml_files = list(self.yaml_dict.keys())

    def build_dirpath(self) -> None:
        """ """

        # Define the mandatory directory tree paths for the respective
        # forecast cycle.
        dirpaths_list = [os.path.join(self.work_path, self.expt_name, self.cycle, "intercom"),
                         os.path.join(self.work_path,
                                      self.expt_name, "com", self.cycle)
                         ]

        # Build the respective directory tree paths.
        for dirpath in dirpaths_list:

            fileio_interface.dirpath_tree(path=dirpath)

    def run(self) -> None:
        """


        """

        # Build the forecast cycle experiment directory tree.
        self.build_dirpath()

        # Define the experiment configuration.
        self.build_config()

# ----


class LaunchError(Error):
    """
    Description
    -----------

    This is the base-class for all exceptions; it is a sub-class of
    Error.

    Parameters
    ----------

    msg: str

        A Python string to accompany the raised exception.

    """

    def __init__(self, msg: str):
        """
        Description
        -----------

        Creates a new LaunchError object.

        """
        super().__init__(msg=msg)
