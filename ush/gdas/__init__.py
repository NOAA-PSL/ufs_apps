# =========================================================================

# Module: ush/gdas/__init__.py

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

    __init__.py

Description
-----------

    This module contains the base-class interface for all Global Data
    Assimilation System (GDAS) applications.

Classes
-------

    GDAS(options_obj)

        This is the base-class object for all Global Data Assimilation
        System (GDAS) applications.

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

    Henry R. Winterbottom; 19 January 2023

History
-------

    2023-01-19: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=unused-argument

# ----

from dataclasses import dataclass

from exceptions import GDASError
from schema import Optional
from tools import parser_interface
from utils import schema_interface
from utils.error_interface import msg_except_handle
from utils.logger_interface import Logger

from gdas.soca.var3d import Global3DVAR as soca_global_3dvar
from gdas.soca.letkf import GlobalLETKF as soca_global_letkf

# ----

# Define the supported applications and respective (supported types);
# for each supported type define the respective Python sub-class
# corresponding to the supported type; an example Python dictionary is
# as follows.

# gdas_configs = {"spam1": {"ham11": eggs11, "ham12": eggs12},
#                 "spam2": {"ham21": eggs21, "ham22": eggs22}
#                }

# In the above example, the "spam" references are the respective GDAS
# applications (i.e., SOCA, GSI, etc.,). The "ham" references are the
# respective GDAS application supported appliction types (e.g.,
# app_type); finally, the "eggs" references are the GDAS sub-classes
# corresponding to the respective (supported) application type.
gdas_configs = {"soca": {"global_3dvar": soca_global_3dvar,
                         "global_letkf": soca_global_letkf}
                }

# ----


@dataclass
class GDAS:
    """
    Description
    -----------

    This is the base-class object for all Global Data Assimilation
    System (GDAS) applications.

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

        Creates a new GDAS object.

        """

        # Define the base-class attributes.
        self.options_obj = options_obj
        self.logger = Logger()

        # Define the supported applications and respective types;
        # verify that the experiment attributes are valid; proceed
        # accordingly.
        if self.options_obj.app.lower() not in gdas_configs:
            msg = (
                f"The GDAS application {self.options_obj.app} is not valid; "
                "the following options are valid: %s. Aborting!!!"
                % [f"{option}" for option in gdas_configs]
            )
            error(msg=msg)

        self.app_type_configs = parser_interface.dict_key_value(
            dict_in=gdas_configs, key=self.options_obj.app.lower(), no_split=True
        )
        if self.options_obj.app_type.lower() not in self.app_type_configs:
            msg = (
                f"The {self.options_obj.app.upper()} application {self.options_obj.app_type} "
                f"is not supported; the following {self.options_obj.app.upper()} application "
                "types are valid %s. Aborting!!!"
                % [f"{option}" for option in self.app_type_configs]
            )
            error(msg=msg)

        msg = (
            f"Executing GDAS {self.options_obj.app.upper()} application "
            f"{self.options_obj.app_type}."
        )
        self.logger.info(msg=msg)

    def run(self) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Defines the appropriate GDAS application and the
            respective application type.

        (2) Executes the GDAS application type.

        """

        # Define the supported GDAS application sub-class and launch
        # the respective application type.
        subcls = parser_interface.dict_key_value(
            dict_in=gdas_configs[self.options_obj.app.lower()],
            key=self.options_obj.app_type.lower(),
        )
        task = subcls(options_obj=self.options_obj)
        task.run()


# ----


@msg_except_handle(GDASError)
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
