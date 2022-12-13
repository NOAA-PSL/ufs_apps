# =========================================================================

# Module: ush/fetch_interface.py

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

from tools import datetime_interface
from tools import fileio_interface
from tools import parser_interface
from utils.error_interface import Error
from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Define the available fetch types; these are the YAML-formatted
# dictionary keys within the base-class attribute fetch_dict; if
# NoneType it is assumed the all specified fetch types provided within
# the configuration file are to be collected.
fetch_types = ['aerosol_obs',
               'atmos_obs',
               'ice_obs',
               'land_obs',
               'ocean_obs'
               ]

# ----


class Fetch():
    """


    """

    def __init__(self, options_obj: object):
        """
        Description
        -----------

        Creates a new Fetch object.

        Raises
        ------

        FetchError:

            * raised if a mandatory argument has not been specified in
              the options_obj attribute provided to the base-class.

        """

        # Define the base-class attributes.
        self.options_obj = options_obj
        self.logger = Logger()

        # Check that the YAML-formatted configuration file exists;
        # proceed accordingly.
        self.yaml_file = parser_interface.object_getattr(
            object_in=self.options_obj, key='yaml_file', force=True)
        if self.yaml_file is None:
            msg = ('The option attributes provided to the base-class does not '
                   'contain the mandatory attribute yaml_file. Aborting!!!')
            raise FetchError(msg=msg)

        exist = fileio_interface.fileexist(path=self.yaml_file)

        if not exist:
            msg = (f'The YAML-formatted configuration file {self.yaml_file} '
                   'does not exist. Aborting!!!')
            raise FetchError(msg=msg)

        # Parse the configuration file.
        self.yaml_dict = fileio_interface.read_yaml(yaml_file=self.yaml_file)

    def build_fetch_dict(self) -> dict:
        """
        Description
        -----------

        This method parses the YAML-formatted configuration file and
        defines the attribute fetch_dict; the respective base-class
        attribute may be further refined in accordance with the
        optional argument fetch_type.

        Returns
        -------

        fetch_dict: dict

            A Python dictionary containing the attributes necessary to
            collect (i.e., fetch) the respective (e.g., specified)
            files.

        Raises
        ------

        FetchError:

            * raised if the dictionary key 'fetch' cannot be
              determined from the YAML-formatted configuration file.

            * raised if the optional fetch type attribute specified
              within the base-class options object is not supported.

        """

        # Collect the fetch configuration attributes; proceed
        # accordingly.
        config_dict = parser_interface.dict_key_value(
            dict_in=self.yaml_dict, key='fetch', force=True)
        if config_dict is None:
            msg = (f'The fetch attribute could not be determined from '
                   f'YAML-formatted configuration file {self.yaml_file}. '
                   'Aborting!!!')
            raise FetchError(msg=msg)

        # Check whether the base-class arguments contain the
        # respective supported fetch types; proceed accordingly
        fetch_type_opt = parser_interface.object_getattr(
            object_in=self.options_obj, key='fetch_type', force=True)

        # If no fetch type has been specified, assume that all values
        # within the file are to be fetched.
        fetch_dict = {}
        if fetch_type_opt is None:

            # Build the Python dictionary containing the fetch
            # attributes accordingly.
            for (key, value) in config_dict.items():
                fetch_dict.update(value)

        # If a fetch type has been specified, proceed accordingly.
        if fetch_type_opt is not None:

            msg = (f'Collecting files for fetch type {fetch_type_opt}.')
            self.logger.warn(msg=msg)

            for fetch_type in fetch_types:

                # If the respective (i.e., allowable) fetch type is
                # determined from the base-class options, proceed
                # accordingly.
                if fetch_type.lower() == fetch_type_opt.lower():
                    fetch_dict = parser_interface.dict_key_value(
                        dict_in=config_dict, key=fetch_type, no_split=True)
                    break

        # Check that the specified observation type is valid; if
        # valid, the Python dictionary will contain attributes
        # collected from the provided configuration file; proceed
        # accordingly.
        if(not bool(fetch_dict)):

            msg = (f'The specified fetch type {fetch_type_opt} is not supported '
                   'or has not been specified in the YAML-formatted configuration '
                   f'file {self.yaml_file}. Aborting!!!')
            raise FetchError(msg=msg)

        return fetch_dict

    def run(self):
        """ """

        # Define the fetching configuration.
        self.fetch_dict = self.build_fetch_dict()


# ----


class FetchError(Error):
    """
    Description
    -----------

    This is the base-class for all exceptions; it is a sub-class of
    Error.

    Parameters
    ----------

    msg: str

        A Python string containing a message to accompany the
        exception.

    """

    def __init__(self, msg: str):
        """
        Description
        -----------

        Creates a new FetchError object.

        """
        super(FetchError, self).__init__(msg=msg)
