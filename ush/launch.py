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
Module
------

    launch.py

Description
-----------

    This module contains classes and methods to create the path and
    configuration files for a respective experiment.

Classes
-------

    Launch(options_obj)

        This is the base-class object for all experiment configuration
        applications.

Functions
---------

    error(msg)

        This function is the exception handler for the respective
        module.

Requirements
------------

- ufs_pyutils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 30 December 2022

History
-------

    2022-12-30: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=no-member
# pylint: disable=unused-argument

# ----

import os

from confs.yaml_interface import YAML
from tools import datetime_interface, fileio_interface, parser_interface
from utils import timestamp_interface
from utils.error_interface import msg_except_handle
from utils.logger_interface import Logger

from exceptions import LaunchError

# ----


class Launch:
    """
    Description
    -----------

    This is the base-class object for all experiment configuration
    applications.

    Parameters
    ----------

    options_obj: object

        A Python object containing the attributes collect via the
        command line from the application driver script.

    Raises
    ------

    LaunchError:

        * raised if the command line arguments do not contain a
          mandatory attribute.

        * raised if the path to the YAML-formatted file specified by
          the command line attribute "yaml_file" does not exist.

    """

    @classmethod
    def __init__(cls, options_obj: object, task_id: str = "launch"):
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
                error(msg=msg)

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
            error(msg=msg)

        # Parse the configuration file.
        self.yaml_dict = YAML().read_yaml(yaml_file=self.yaml_file)

        # Define the directory tree paths relative to the respective
        # forecast cycle.
        print(self.work_path)
        quit()

        self.com_root = os.path.join(
            self.work_path, self.expt_name, "com", self.cycle)
        self.itrc_root = os.path.join(
            self.work_path, self.expt_name, self.cycle, "intercom"
        )

        # Define the YAML-formatted experiment configuration file for
        # the respective task.
        self.yaml_config_path = f"{task_id}.{self.expt_name}.{self.cycle}.yaml"

        msg = f"The YAML-formatted experiment configuration file name is {self.yaml_config_path}."
        self.logger.warn(msg=msg)

    def build_configs(self) -> None:
        """
        Description
        -----------

        This method builds the YAML-formatted experiment configuration
        files within the respective experiment /com and /intercom
        paths.

        Raises
        -------

        LaunchError:

            * raised if a mandatory experiment attribute has not been
              defined.

        """

        # Define the mandatory experiment attributes within the
        # YAML-formatted configuration file.
        attrs_list = [
            "com_root",
            "cycle",
            "expt_name",
            "itrc_root",
            "work_path",
        ]

        # Create the respective configuration files.
        config_files_list = [
            os.path.join(self.com_root, self.yaml_config_path),
            os.path.join(self.itrc_root, self.yaml_config_path),
        ]

        for config_file in config_files_list:

            # Compile a list of YAML-formatted files collected from
            # the experiment configuration; it not a YAML-formatted
            # file, update the Python dictionary with the respective
            # key and value pair.
            (in_dict, yaml_file_list) = ({}, [])

            # Check that the respective attribute value; proceed
            # accordingly.
            for (attr_key, attr_value) in self.yaml_dict.items():

                # If the respective attribute is a YAML-formatted
                # file, update the list of YAML-formatted files to be
                # concatenated.
                if YAML().check_yaml(attr_value=attr_value):
                    if fileio_interface.fileexist(path=attr_value):
                        yaml_file_list.append(attr_value)

                if not YAML().check_yaml(attr_value=attr_value):
                    value = parser_interface.dict_key_value(
                        dict_in=self.yaml_dict, key=attr_key, no_split=True
                    )
                    in_dict[attr_key] = value

            # Add the experiment attributes to the YAML-formatted
            # configuration file; proceed accordingly.
            for attr in attrs_list:
                value = parser_interface.object_getattr(
                    object_in=self, key=attr, force=True
                )
                if value is None:
                    msg = (
                        f"The mandatory attribute {attr} has not been "
                        "specified. Aborting!!!"
                    )
                    error(msg=msg)
                in_dict[attr] = value

            # Concatenate the respective YAML-formatted files list and
            # subsequently write all configuration attributes to the
            # respetive YAML-formatted configuration file.
            YAML().concat_yaml(
                yaml_file_list=yaml_file_list,
                yaml_file_out=config_file,
                ignore_missing=True,
            )
            YAML().write_yaml(yaml_file=config_file, in_dict=in_dict, append=True)

            timestamp = datetime_interface.current_date(
                frmttyp=timestamp_interface.INFO, is_utc=True
            )
            with open(config_file, "a", encoding="utf-8") as file:
                file.write(f"\n# Created {timestamp} from {self.yaml_file}.\n")

    def build_dirpath(self) -> None:
        """
        Description
        -----------

        This method builds the directory path tree for the respective
        experiment.

        """

        # Define the mandatory directory tree paths for the respective
        # forecast cycle.
        dirpaths_list = [
            os.path.join(self.work_path, self.expt_name, self.cycle, "intercom"),
            os.path.join(self.work_path, self.expt_name, "com", self.cycle),
        ]

        # Build the respective directory tree paths.
        for dirpath in dirpaths_list:
            msg = f"Building directory tree {dirpath}."
            self.logger.info(msg=msg)
            fileio_interface.dirpath_tree(path=dirpath)

    def run(self) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Builds the directory tree for the respective experiment.

        (2) Builds the YAML-formatted experiment configuration files
            for the respective experiment.

        """

        # Build the forecast cycle experiment directory tree.
        self.build_dirpath()

        # Define the experiment configuration.
        self.build_configs()


# ----


@msg_except_handle(LaunchError)
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
