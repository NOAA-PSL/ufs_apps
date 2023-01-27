# =========================================================================

# Module: ush/gdas/soca/var3d.py

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
from gdas.soca import SOCA, error
from tools import datetime_interface
from tools import fileio_interface
from tools import parser_interface
from utils import timestamp_interface

# ----


class Global3DVAR(SOCA):
    """
    Description
    -----------

    This is the base-class object for all Sea-ice and Ocean Coupled
    Analysis (SOCA) global 3-dimensional variational (3DVAR)
    applications; it is a sub-class of SOCA.

    Parameters
    ----------

    options_obj: object

        A Python object containing the attributes collect via the
        command line from the application driver script.

    """

    def __init__(self, options_obj: object):
        """
        Description
        -----------

        Creates a new Global3DVAR object.

        """

        # Define the base-class attributes.
        task_id = "global_soca_3dvar"
        super().__init__(options_obj=options_obj,
                         task_id="global_soca_3dvar"
                         )
        self.dirpath = os.path.join(self.expt_path, "soca", task_id)
        self.build_dirtree(path=self.dirpath)
        os.chdir(self.dirpath)

        # Define the mandatory configuration variables.
        self.config_var_list = ["analysis_variables", "state_variables"]

        # Define the YAML-formatted files for the SOCA application.
        self.soca_berror_yaml = os.path.join(
            self.dirpath, "soca_berror.yaml")
        self.soca_bkgrds_yaml = os.path.join(
            self.dirpath, "soca_backgrounds.yaml")
        self.soca_config_yaml = os.path.join(
            self.dirpath, "soca.global_3dvar.yaml")
        self.soca_observations_yaml = os.path.join(
            self.dirpath, "soca_observations.yaml")

        # Define a Python dictionary containing the default values for
        # the respective SOCA application; these attributes will be
        # queried and defined as run-time environment variables
        # accordingly.
        self.soca_default_attrs = {"atm_window_begin": datetime_interface.datestrupdate(
            datestr=self.launch.cycle,
            in_frmttyp=timestamp_interface.GLOBAL,
            out_frmttyp=timestamp_interface.Y_m_dTHMSZ,
            offset_seconds=float(self.soca_config_obj.analysis_interval_seconds/2.0)),
            "atm_window_length": f"PT{self.soca_config_obj.analysis_interval_seconds}S",
            "ninner": 100
        }

    def config_soca(self) -> None:
        """
        Description
        -----------

        This method configures the SOCA application; this includes the
        building of the respective configuration and YAML-formatted
        SOCA application files as well as fixed-file collection.

        """

        # Check that the SOCA application configuration contains (at
        # least) the mandatory attributes.
        self.check_mandvars(mandvar_list=self.config_var_list)

        # Build the external files to be used for compiling the SOCA
        # application configuration file.
        config_file_dict = {os.path.join(self.dirpath, "analysis_variables.yaml"):
                            self.soca_config_obj.analysis_variables,
                            os.path.join(self.dirpath, "state_variables.yaml"):
                            self.soca_config_obj.state_variables
                            }

        self.build_config_files(config_file_dict=config_file_dict)

        # Create the background-error YAML-formatted file.
        self.berror_config(berror_filepath=self.soca_berror_yaml)

        # Establish the environment variables and values required to
        # build the YAML-formatted SOCA application configuration
        # file; proceed accordingly.
        for config_var in self.config_var_list:
            value = parser_interface.object_getattr(
                object_in=self.soca_config_obj, key=config_var, force=True)
            if value is None:
                msg = (f"The SOCA configuration attribute {config_var} cannot "
                       "be NoneType. Aborting!!!")
                error(msg=msg)

        for soca_attr in self.soca_default_attrs:
            value = parser_interface.object_getattr(
                object_in=self.soca_config_obj, key=soca_attr, force=True)
            if value is None:
                value = parser_interface.dict_key_value(
                    dict_in=self.soca_default_attrs, key=soca_attr, force=True,
                    no_split=True)

                if value is None:
                    msg = (f"The SOCA attribute {soca_attr} cannot be NoneType. "
                           "Aborting!!!")
                    error(msg=msg)

            parser_interface.enviro_set(envvar=soca_attr.upper(),
                                        value=str(value))

        # Build the YAML-formatted SOCA application configuration
        # file.
        yaml_dict = YAML().read_yaml(yaml_file=self.soca_config_obj.soca_config)
        YAML().write_yaml(yaml_file=self.soca_config_yaml, in_dict=yaml_dict)

    def run(self) -> None:
        """

        """

        # Build the directory tree for the respective application.
        self.build_dirtree(dirpath=self.dirpath, is_ens=False)

        # Link the SOCA application fixed files.
        self.link_fixedfiles(
            dirpath=self.dirpath,
            fixedfile_yaml=self.soca_config_obj.fixed_file_config,
            ignore_missing=False)

        # Link the background forecast files.
        self.build_bkgrds_fgat(dirpath=self.dirpath,
                               soca_fgat_file=self.soca_bkgrds_yaml)

        # Link and configure the observation attributes.
        self.build_obs(dirpath=self.dirpath,
                       obs_config_yaml=self.soca_config_obj.obs_config,
                       soca_obs_file=self.soca_observations_yaml)

        # Configure the SOCA application.
        self.config_soca()
