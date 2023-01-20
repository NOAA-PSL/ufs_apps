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


"""

# ----


# ----

from confs.yaml_interface import YAML
from launch import Launch
from tools import datetime_interface, fileio_interface, parser_interface
from utils import timestamp_interface
from utils.error_interface import msg_except_handle
from utils.logger_interface import Logger

from exceptions import SOCAError

# ----


class SOCA:
    """

    """

    @classmethod
    def __init__(cls, options_obj: object, task_id: str = None):
        """
        Description
        -----------

        Creates a new SOCA object.

        """

        # Define the base-class attributes.
        self = cls
        self.options_obj = options_obj
        self.logger = Logger()
        self.launch = Launch(options_obj=self.options_obj, task_id=task_id)
        self.launch.build_dirpath()
        self.launch.build_configs()

    def build_dirtree(self, dirpath: str, is_ens: bool = False) -> None:
        """ """


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
