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
        self.logger = Logger()

        # Parse the YAML-formatted file and configure the SOCA
        # application; proceed accordingly.
        self.yaml_dict = YAML().read_concat_yaml(yaml_file=self.options_obj.yaml_file)
        soca_app_dict = parser_interface.dict_key_value(
            dict_in=self.yaml_dict, key="soca", force=True, no_split=True)
        if soca_app_dict is None:
            msg = (f"The experiment configuration file {self.options_obj.yaml_file} "
                   "does not contain the attribute 'soca'. Aborting!!!")
            error(msg=msg)

        self.soca_config_obj = parser_interface.object_define()
        for soca_item in soca_app_dict:
            value = parser_interface.dict_key_value(
                dict_in=soca_app_dict, key=soca_item, no_split=True)
            self.soca_config_obj = parser_interface.object_setattr(
                object_in=self.soca_config_obj, key=soca_item, value=value)

    def build_config_files(self, config_file_dict):
        """

        """

        # Build each configuration file accordingly.
        for config_file in config_file_dict:

            # Define the values for the configuration file and write
            # the values to the respective configuration file; proceed
            # accordingly.
            value = parser_interface.dict_key_value(
                dict_in=config_file_dict, key=config_file, no_split=True)

            try:
                with open(config_file, "w", encoding="utf-8") as file:
                    if isinstance(value, list):
                        file.write(
                            "[" + ",".join([item for item in value]) + "]")
                    if not isinstance(value, list):
                        file.write(value)

            except Exception as errmsg:
                msg = (f"Writing the configuration file {config_file} failed "
                       f"with error {errmsg}. Aborting!!!")
                error(msg=msg)

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
            subdirs_list = [subdirs_list.append(subdir) for subdir
                            in ["ensemble", "letkf_observer_obs", "letkf_solver_obs",
                                "update"]]

        # Build the directory tree path(s).
        for subdir in subdirs_list:
            path = os.path.join(dirpath, subdir)
            fileio_interface.dirpath_tree(path=path)

    def build_obs(self, dirpath: str, obs_config_yaml: str,
                  soca_obs_file: str) -> None:
        """
        Description
        -----------

        This method builds the YAML-formatted observation
        configuration files for each specified observation (and
        associated attributes) defined in the obs_config attribute of
        the SOCA application experiment configuration file; the file
        path names are written to a YAML-formatted file containing
        attributes allowing the file to be parsed using the
        transclusion applications of the YAML parser toolkit (see
        ufs_pyutils/confs/yaml_interface.py).

        Parameters
        ----------

        dirpath: str

            A Python string specifying the top-level directory path
            beneath which the sub-directory tree will be built.

        obs_config_yaml: str

            A Python string specifying the path to the YAML-formatted
            file contain the observation attributes.

        soca_obs_file: str

            A Python string specifying the path to the YAML-formatted
            file to contain the transclusion paths for the respective
            SOCA observations for assimilation; this file path is
            defined in the sub-class constructor.

        """

        # Check that the observation configuration file exists;
        # proceed accordingly.
        exist = fileio_interface.fileexist(path=obs_config_yaml)
        if not exist:
            msg = (f"The YAML-formatted file path {obs_config_yaml} does not "
                   "exist. Aborting!!!")
            error(msg=msg)

        # Parse the YAML-formatted observation configuration file and
        # proceed accordingly.
        obs_yaml_dict = YAML().read_yaml(yaml_file=obs_config_yaml)
        if obs_yaml_dict is None:
            msg = ("The SOCA observation attributes cannot be determined from "
                   f"file {obs_config_yaml}. Aborting!!!")
            error(msg=msg)

        # Configure the respective observation(s) for the GDAS SOCA
        # application.
        obs_yaml_list = []
        for ob_types in obs_yaml_dict:

            # Define the attributes required to build the respective
            # YAML-formatted files for the SOCA application; proceed
            # accordingly.
            msg = (f"Building YAML-formatted configuration file(s) for {ob_types} "
                   "observations.")
            self.logger.info(msg=msg)

            ob_types_dict = parser_interface.dict_key_value(
                dict_in=obs_yaml_dict, key=ob_types, force=True)
            if ob_types_dict is None:
                msg = ("The observation attributes could not be determined "
                       f"for observation type {ob_types} from YAML-formatted "
                       f"file path {obs_config_yaml}. Aborting!!!")
                error(msg=msg)

            for ob_type in ob_types_dict:
                obs_dict = parser_interface.dict_key_value(
                    dict_in=ob_types_dict, key=ob_type, force=True)
                if obs_dict is None:
                    msg = ("Observation attributes could not be determined for "
                           f"observation type {ob_type} within YAML-formatted "
                           f"file path {obs_config_yaml}. Aborting!!!")
                    error(msg=msg)

                for obs_attr in obs_dict:

                    # Define the environment variables using the
                    # attributes for the respective observation type.
                    value = parser_interface.dict_key_value(
                        dict_in=obs_dict, key=obs_attr, no_split=True)
                    value = datetime_interface.datestrupdate(
                        datestr=self.launch.cycle,
                        in_frmttyp=timestamp_interface.GLOBAL,
                        out_frmttyp=value,
                        offset_seconds=self.soca_config_obj.analysis_interval_seconds)
                    parser_interface.enviro_set(envvar=obs_attr.upper(),
                                                value=value)

                # Generate the YAML-formatted file containing the SOCA
                # application configuration; proceed accordingly.
                yaml_file = parser_interface.dict_key_value(
                    dict_in=obs_dict, key="yaml_tmpl", force=True, no_split=True)
                if yaml_file is None:
                    msg = ("A YAML-template file path has not been specified for observation "
                           f"type {ob_type} in file path {obs_config_yaml}. Aborting!!!"
                           )
                    error(msg=msg)

                exist = fileio_interface.fileexist(path=yaml_file)
                if not exist:
                    msg = (f"The YAML-formatted file path {yaml_file} for observation type "
                           f"{ob_type} does not exist. Aborting!!!")
                    error(msg=msg)

                obs_config_yaml = os.path.join(dirpath, f"{ob_type}.yaml")
                msg = f"Building SOCA YAML-formatted observation configuration file {obs_config_yaml}."
                self.logger.info(msg=msg)
                yaml_dict = YAML().read_yaml(yaml_file=yaml_file)
                YAML().write_yaml(yaml_file=obs_config_yaml, in_dict=yaml_dict)

                # Update the Python list containing the file paths for
                # the respective YAML-formatted files.
                obs_yaml_list.append(obs_config_yaml)

        # Build a YAML-formatted file containing the observation file
        # paths.
        with open(soca_obs_file, "w", encoding="utf-8") as file:
            for obs_yaml in obs_yaml_list:
                msg = (
                    f"Writing transclusion attributes for observation file path {obs_yaml}.")
                self.logger.info(msg=msg)
                file.write(f"- !INC {obs_yaml}\n")

    def check_mandvars(self, mandvar_list):
        """ """

        missing_vars = list(
            sorted(set(mandvar_list) - set(vars(self.soca_config_obj))))

        if len(missing_vars) > 0:
            msg = ("The following mandatory SOCA configuration variables have not been "
                   "specified in the experiment configuration file path "
                   f"{self.options_obj.yaml_file}: {missing_vars}. Aborting!!!")
            error(msg=msg)


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
