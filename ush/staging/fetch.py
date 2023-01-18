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
Module
------

    fetch.py

Description
-----------

    This module contains classes and methods relative to fetch
    application.

Classes
-------

    Fetch(options_obj)

        This is the base-class object for all file fetching (e.g.,
        downloading) and processing (if applicable) applications; it
        is a subclass of Staging.

Requirements
------------

- ufs_pyutils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 17 December 2022

History
-------

    2022-12-17: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=attribute-defined-outside-init
# pylint: disable=no-member

# ----

from tools import parser_interface

from staging import Staging
from staging import error as staging_error

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Define the default AWS fetch attribute values.
aws_opt_attr_dict = {
    "bufr_concat": None,
    "ignore_missing": True,
    "multifile": None,
    "nc_concat": None,
    "offset_seconds": 0,
    "profile_name": None,
    "stream_start": 19000101000000,
    "stream_stop": 20991231230000,
}

# Define the mandatory AWS fetch attribute values.
aws_mand_attr_list = ["bucket", "local_path", "object_path"]

# -----


class Fetch(Staging):
    """
    Description
    -----------

    This is the base-class object for all file fetching (e.g.,
    downloading) and processing (if applicable) applications; it is a
    subclass of Staging.

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

        Creates a new Fetch object.

        """

        # Define the supported fetch application interfaces.
        task_id = str()
        self.fetch_methods_dict = {"aws_s3": self.aws_s3}

        # Check whether the base-class arguments contain the
        # respective supported fetch types; proceed accordingly
        self.fetch_type_opt = parser_interface.object_getattr(
            object_in=options_obj, key="fetch_type", force=True
        )

        # Define the interface/platform types to be collected.
        self.platforms = self._get_platforms()
        print(self.platforms)

        # Define the file identifiers to be collected.
        self.fileids = self._get_fileids()

        # Define the base-class attributes.
        super().__init__(options_obj=options_obj)

        print(self.fileids)

        quit()

    def _get_fetch_types(self) -> list:
        """
        Description
        -----------

        This method defines a list of fetch types in accordance with
        the base-class attributes.

        Returns
        -------

        fetch_types_list: list

            A Python list of fetch types determined in accordance with
            the base-class attributes.

        """

        # Define a list of unique fetch types in accordance with the
        # base-class attributes.
        fetch_types_list = list(set(self.fetch_type_opt.split(",")))

        # Check if list is empty; proceed accordingly.
        if not fetch_types_list:
            msg = (
                "The fetch types list is empty and/or cannot be determine "
                "from the base-class attributes. Aborting!!!"
            )
            staging_error(msg=msg)

        return fetch_types_list

    def _get_fileids(self) -> list:
        """
        Description
        -----------

        This method defines the base-class attribute fileids with
        respect to the command line option attribute fileid.

        Returns
        -------

        fileids: list

            A Python list of file identifiers to be collected.

        """

        # Check whether the base-class arguments contain the file
        # identifier attribute; proceed accordingly.
        fileids = None
        fileid_opt = parser_interface.object_getattr(
            object_in=self.options_obj, key="fileid", force=True
        )

        # If the file identifier attribute has been specified, define
        # a list of values to be returned.
        if fileid_opt is not None:

            fileids = list(set(fileid_opt.split(",")))

        return fileids

    def _get_platforms(self) -> list:
        """
        Description
        -----------

        This method defines the base-class attribute platforms with
        respect to the command line option attribute platform.

        Returns
        -------

        platforms: list

            A Python list of interface/platforms to be collected.

        Raises
        ------

        StagingError:

            * raised if a specified platform is not supported by this
              application.

        """

        # Check whether the base-class arguments contain the
        # respective interface/platform type; proceed accordingly.
        platform_opt = parser_interface.object_getattr(
            object_in=self.options_obj, key="platform", force=True
        )

        if platform_opt is None:

            # Define a list of interface/platform types using the
            # base-class attributes.
            platforms = list(self.fetch_methods_dict.keys())

        if platform_opt is not None:

            # Define a list of unique interface/platform types.
            platforms = list(set(platform_opt.split(",")))

            # Check that the interface/platform is supported; proceed
            # accordingly.
            for platform in platforms:
                if platform not in self.fetch_methods_dict:
                    msg = f"The interface/platform type {platform} is not supported. Aborting!!!"
                    staging_error(msg=msg)

        return platforms

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

        # Check whether file identifiers have been specified; proceed
        # accordingly.
        if self.fileids is not None:

            # Define a Python dictionary containing only the specified
            # file identifiers and overwrite the Python dictionary
            # specified upon entry; proceed accordingly.
            tmpdict = {}
            # fileids = [item for item in self.fileids if item in
            #           list(filesdict.keys())]
            for fileid in self.fileids:

                if fileid in filesdict:  # list(filesdict.keys()):
                    tmpdict[fileid] = parser_interface.dict_key_value(
                        dict_in=filesdict, key=fileid, force=True, no_split=True
                    )

                if fileid not in filesdict:  # list(filesdict.keys()):
                    msg = (
                        f"Attributes for file identifier {fileid} could "
                        "not be determined from the configuration file "
                        "and will not be collected."
                    )
                    self.logger.warn(msg=msg)

            filesdict = tmpdict
            if len(filesdict.keys()) <= 0:
                msg = (
                    "No valid file identifiers has been specified; "
                    "nothing will be collected."
                )
                self.logger.warn(msg=msg)

                return None

        # Collect the AWS s3 checksum index attributes.
        checksum_obj = parser_interface.object_define()
        checksum_attrs_dict = {"aws_s3_filepath": None, "aws_s3_hash": "md5"}

        for (checksum_attr, _) in checksum_attrs_dict.items():
            value = parser_interface.dict_key_value(
                dict_in=self.checksum_dict, key=checksum_attr, force=True, no_split=True
            )

            if value is None:

                value = parser_interface.dict_key_value(
                    dict_in=checksum_attrs_dict,
                    key=checksum_attr,
                    force=True,
                    no_split=True,
                )

            checksum_obj = parser_interface.object_setattr(
                object_in=checksum_obj, key=checksum_attr, value=value
            )

        # Loop through all AWS s3 files to be collected; proceed
        # accordingly.
        for fileid in filesdict.keys():

            # Build the Python object containing the experiment
            # configuration attributes for the respective file(s) to
            # be collected.
            fileid_obj = self.build_fileid_obj(
                filesdict=filesdict,
                fileid=fileid,
                mand_attr_list=aws_mand_attr_list,
                opt_attr_dict=aws_opt_attr_dict,
            )

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
                checksum_index=checksum_index,
                checksum_level=checksum_obj.aws_s3_hash,
            )

            # If applicable, concatenate the respective files in
            # accordance with the experiment configuration.
            self.concat_filepath(fileid_obj=fileid_obj)

        return None

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

        """

        # Collect the fetch configuration attributes; proceed
        # accordingly.
        fetch_dict = parser_interface.dict_key_value(
            dict_in=self.yaml_dict, key="fetch", force=True
        )

        if fetch_dict is None:
            msg = (
                f"The fetch attribute could not be determined from "
                f"YAML-formatted configuration file {self.yaml_file}. "
                "Aborting!!!"
            )
            staging_error(msg=msg)

        return fetch_dict

    def collect(self, fetch_dict: dict) -> None:
        """
        Description
        -----------

        This method collects the specified files for the respective
        interface/platform; all processing is done via the respective
        method corresponding to the interface/platform fetching
        method.

        Parameters
        ----------

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

            * raised if the specified fetch method (i.e.,
              platform/interface) is not supported.

        """

        # Collect the checksum information from the configuration file
        # attributes.
        self.get_checksum_info(fetch_dict=fetch_dict)

        # For each supported interface/platform type, collect (i.e.,
        # fetch) the attributes specified in the YAML-formatted
        # configuration file.
        for fetch_method in self.platforms:

            # Define the base-class method to be used for collecting
            # from the supported interfaces/platforms; proceed
            # accordingly.
            method = parser_interface.dict_key_value(
                dict_in=self.fetch_methods_dict,
                key=fetch_method,
                force=True,
                no_split=True,
            )

            if method is None:
                msg = (
                    f"A method for collecting files from the {fetch_method} "
                    "platform is not supported. Aborting!!!"
                )
                staging_error(msg=msg)

            # Define the respective file attributes for the respective
            # supported interface/platform.
            filesdict = parser_interface.dict_key_value(
                dict_in=fetch_dict, key=fetch_method, force=True, no_split=True
            )

            # Parse the configuration file attributes in accordance
            # with the base-class argument; proceed accordingly.
            if self.fetch_type_opt is None:
                fetch_types = list(filesdict.keys())

            if self.fetch_type_opt is not None:
                fetch_types = self._get_fetch_types()

            # Collect files in accordance with the configuration and
            # options.
            for fetch_type in fetch_types:

                if fetch_type in filesdict:
                    msg = f"Collecting files for fetch type {fetch_type}."
                    self.logger.info(msg=msg)
                    method(filesdict=filesdict[fetch_type])

                if fetch_type not in filesdict:
                    msg = (
                        "The configuration file does not specify a key "
                        f"for fetch type {fetch_type}; {fetch_type} files "
                        "will not be collected."
                    )
                    self.logger.warn(msg=msg)

    def get_checksum_info(self, fetch_dict: dict) -> None:
        """
        Description
        -----------

        This method collects the checksum attributes for each
        platform/interface (if applicable) from the YAML-formatted
        configuration file and defines the base-class attributes
        checksum and checksum_dict; if the checksum YAML-block is not
        specified within the YAML-formatted configuration files, not
        checksum hash values will be defined/determined during the
        respective fetching application.

        Parameters
        ----------

        fetch_dict: dict

            A Python dictionary containing the attributes necessary to
            collect (i.e., fetch) the respective (e.g., specified)
            files; the dictionary keys correspond to the respective
            fetching method (see the base-class attribute
            fetch_methods_dict) and the corresponding values are the
            YAML-formed dictionaries for the respective files to be
            retrieved by the respective fetching method.

        """

        # Define the checksum hash attributes for the respective
        # fetching interfaces; proceed accordingly.
        self.checksum_dict = parser_interface.dict_key_value(
            dict_in=fetch_dict, key="checksum", force=True, no_split=True
        )

        if self.checksum_dict is None:
            msg = (
                "The checksum attributes for fetched files has not "
                f"specified in {self.yaml_file}; checksum hash values "
                "will only be written to standard output."
            )
            self.logger.warn(msg=msg)
            self.checksum = False

        if self.checksum_dict is not None:
            self.checksum = True

    def run(self) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Collects and defines the local attributes determined from
            the YAML-formatted configuration file relative to the
            fetch application.

        (2) For each supported platform/interface collects (e.g.,
            fetches) the specified files in accordance with to any
            options specified/defined within the YAML-formatted
            configuration file.

        """

        # Define the fetching configuration.
        fetch_dict = self.build_fetch_dict()

        # Collect the specified files for each interface.
        self.collect(fetch_dict=fetch_dict)
