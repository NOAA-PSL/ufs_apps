# =========================================================================

# Module: ush/staging/fetch.py

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

from staging import Staging
from staging import StagingError
from tools import datetime_interface
from tools import fileio_interface
from tools import parser_interface
from tools import system_interface

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class Fetch(Staging):
    """


    """

    def __init__(self, options_obj: object):
        """
        Description
        -----------

        Creates a new Fetch object.

        Raises
        ------

        StagingError:

            * raised if a mandatory argument has not been specified in
              the options_obj attribute provided to the base-class.

        """

        # Define the base-class attributes.
        super().__init__(options_obj=options_obj)

        # Define the supported fetch application interfaces.
        self.fetch_methods_dict = {'aws_s3': self.aws_s3,
                                   'noaa_hpss': self.aws_s3}  # None}

        # Check whether the base-class arguments contain the
        # respective supported fetch types; proceed accordingly
        self.fetch_type_opt = parser_interface.object_getattr(
            object_in=self.options_obj, key='fetch_type', force=True)

    def aws_s3(self, filesdict):
        """
        Description
        -----------

        This method collects files specified within the YAML-formatted
        configuration file that are hosted within an Amazon Web
        Services (AWS) s3 bucket and object path.

        Parameters
        ----------

        filesdict: dict

            A Python dictionary containing the local and remote paths
            for the files to be collected from AWS s3; the Python
            dictionary keys are the local host path(s) for the
            collected files while the Python dictionary values are the
            AWS s3 object paths.

        """

        # Collect the AWS s3 checksum index attributes.
        checksum_obj = parser_interface.object_define()
        checksum_attrs_dict = {'aws_s3_filepath': None,
                               'aws_s3_hash': 'md5'
                               }

        for checksum_attr in checksum_attrs_dict.keys():
            value = parser_interface.dict_key_value(
                dict_in=self.checksum_dict, key=checksum_attr,
                force=True, no_split=True)

            if value is None:

                value = parser_interface.dict_key_value(
                    dict_in=checksum_attrs_dict, key=checksum_attr,
                    force=True, no_split=True)

            checksum_obj = parser_interface.object_setattr(
                object_in=checksum_obj, key=checksum_attr, value=value)

        # Loop through all AWS s3 files to be collected; proceed
        # accordingly.
        for fileid in filesdict.keys():

            # Build the Python object containing the experiment
            # configuration attributes for the respective file(s) to
            # be collected.
            fileid_obj = self.build_awss3_fileid_obj(
                filesdict=filesdict, fileid=fileid)

            # Define list of valid timestamps relative to the
            # respective file attributes.
            fileid_obj = self.get_timestamps_list(fileid_obj=fileid_obj)

            # Collect the respective file(s) from AWS s3 and update
            # the external file accordingly.
            if checksum_obj.aws_s3_filepath is None:
                checksum_index = False

            if checksum_obj.aws_s3_filepath is not None:
                checksum_index = True

            self.awss3_fetch(
                fileid_obj=fileid_obj,
                checksum_filepath=checksum_obj.aws_s3_filepath,
                checksum_index=checksum_index, checksum_level=checksum_obj.aws_s3_hash)

            # If applicable, concatenate the respective files in
            # accordance with the experiment configuration.
            self.concat_filepath(fileid_obj=fileid_obj)

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
            files; the dictionary keys correspond to the respective
            fetching method (see the base-class attribute
            fetch_methods_dict) and the corresponding values are the
            YAML-formed dictionaries for the respective files to be
            retrieved by the respective fetching method.

        Raises
        ------

        StagingError:

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
            raise StagingError(msg=msg)

        # Build the Python dictionary containing the fetch attributes.
        fetch_dict = {}
        for (fetch_method, _) in self.fetch_methods_dict.items():

            # Define the file attributes for the respective fetch
            # application (i.e., supported interface or platform).
            fetch_dict[fetch_method] = dict()
            for (key, value) in config_dict[fetch_method].items():
                fetch_dict[fetch_method][key] = value

        return fetch_dict

    def collect(self, fetch_dict: dict) -> None:
        """ 

        """

        # For each supported interface/platform type, collect (i.e.,
        # fetch) the attributes specified in the YAML-formatted
        # configuration file.
        for (fetch_method, _) in fetch_dict.items():

            # Define the base-class method to be used for collecting
            # from the supported interfaces/platforms; proceed
            # accordingly.
            method = parser_interface.dict_key_value(
                dict_in=self.fetch_methods_dict, key=fetch_method, force=True,
                no_split=True)

            if method is None:
                msg = (f'A method for collecting files from the {fetch_method} '
                       'platform is not supported. Aborting!!!')
                raise StagingError(msg=msg)

            # Define the respective file attributes for the respective
            # supported interface/platform.
            filesdict = parser_interface.dict_key_value(
                dict_in=fetch_dict, key=fetch_method, force=True, no_split=True)

            # Parse the configuration file attributes in accordance
            # with the base-class argument; proceed accordingly.
            if self.fetch_type_opt is None:
                fetch_types = list(filesdict.keys())

            if self.fetch_type_opt is not None:
                fetch_types = [self.fetch_type_opt]

            # Collect files in accordance with the configuration and
            # options.
            for fetch_type in fetch_types:

                # add method here

    def run(self):
        """ """

        # Define the fetching configuration.
        fetch_dict = self.build_fetch_dict()

        # Collect the specified files for each interface.
        self.collect(fetch_dict=fetch_dict)
