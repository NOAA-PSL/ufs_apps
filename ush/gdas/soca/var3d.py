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
from tools import fileio_interface
from tools import parser_interface

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

        # Define the mandatory configuration variables.
        self.config_var_list = ["analysis_variables", "state_variables"]

        # Collect the configuration attributes.
        # self.soca_app_config = parser_interface.object_define()

        # Define the YAML-formatted file to contain the observations
        # for the SOCA application.
        self.soca_observations_yaml = os.path.join(
            self.dirpath, "soca_observations.yaml")
        self.soca_config_yaml = os.path.join(
            self.dirpath, "soca.global_3dvar.yaml")

    def config_soca(self) -> None:
        """ """
        os.chdir(self.dirpath)

        # Check that the SOCA application configuration contains (at
        # least) the mandatory attributes.
        self.check_mandvars(mandvar_list=self.config_var_list)

        # Establish the environment variables and values required to
        # build the YAML-formatted SOCA application configuration
        # file.
        for config_var in self.config_var_list:
            value = parser_interface.object_getattr(
                object_in=self.soca_config_obj, key=config_var, force=True)
            if value is None:
                msg = (f"The SOCA configuration attribute {config_var} cannot "
                       "be NoneType. Aborting!!!")
                error(msg=msg)

            parser_interface.enviro_set(envvar=config_var.upper(), value=value)

        # Build the YAML-formatted SOCA application configuration
        # file.
        yaml_dict = YAML().read_yaml(yaml_file=self.soca_config_obj.soca_config)
        YAML().write_yaml(yaml_file=self.soca_config_yaml, in_dict=yaml_dict)

    def run(self) -> None:
        """

        """

        # Build the directory tree for the respective application.
        self.build_dirtree(dirpath=self.dirpath, is_ens=False)

        # Link and configure the observation attributes.
        self.build_obs(dirpath=self.dirpath,
                       obs_config_yaml=self.soca_config_obj.obs_config,
                       soca_obs_file=self.soca_observations_yaml)

        # Configure the SOCA application.
        self.config_soca()
