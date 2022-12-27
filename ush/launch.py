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
        self.yaml_dict = YAML().read_yaml(yaml_file=self.yaml_file)

        # Define the directory tree paths relative to the respective
        # forecast cycle.
        self.com_root = os.path.join(
            self.work_path, self.expt_name, "com", self.cycle)
        self.itrc_root = os.path.join(
            self.work_path, self.expt_name, self.cycle, "intercom")

        # Define the JSON- and YAML-formatted experiment configuration
        # files.
        self.json_config_path = f"ufs.{self.expt_name}.{self.cycle}.json"
        self.yaml_config_path = f"ufs.{self.expt_name}.{self.cycle}.yaml"

    def build_configs(self) -> None:
        """ """

        # Define the configuration file paths.
        config_files = [os.path.join(path, filename) for filename in [
            self.json_config_path, self.yaml_config_path] for path in self.dirpaths_list]

        # Define the YAML-formatted file attributes.
        yaml_file_list = [filename for (_, filename) in self.yaml_dict.items()]

        # Build the concatenated YAML-formatted files.
        for config_file in config_files:

            if ".yaml" in config_file.lower():

                YAML().concat_yaml(yaml_file_list=yaml_file_list, yaml_file_out=config_file,
                                   fail_nonvalid=False, ignore_missing=True)

    def build_dirpath(self) -> None:
        """ """

        # Define the mandatory directory tree paths for the respective
        # forecast cycle.
        self.dirpaths_list = [os.path.join(self.work_path, self.expt_name, self.cycle, "intercom"),
                              os.path.join(self.work_path,
                                           self.expt_name, "com", self.cycle)
                              ]

        # Build the respective directory tree paths.
        for dirpath in self.dirpaths_list:

            msg = f"Building directory tree {dirpath}."
            self.logger.info(msg=msg)
            fileio_interface.dirpath_tree(path=dirpath)

    def run(self) -> None:
        """


        """

        # Build the forecast cycle experiment directory tree.
        self.build_dirpath()

        # Define the experiment configuration.
        self.build_configs()

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
