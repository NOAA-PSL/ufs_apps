# =========================================================================

# Module: ush/staging/__init__.py

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

    This module contains classes and methods relative to staging
    (i.e., fetching and storing) application.

Classes
-------

    Staging(options_obj)

        This is the base-class object for all staging (i.e., fetching
        and storing) applications.

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

    Henry R. Winterbottom; 17 December 2022

History
-------

    2022-12-17: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=no-member
# pylint: disable=too-many-lines
# pylint: disable=unused-argument

# ----

import os

import numpy
from confs.yaml_interface import YAML
from exceptions import StagingError
from ioapps import boto3_interface, hashlib_interface, netcdf4_interface
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


class Staging:
    """
    Description
    -----------

    This is the base-class object for all staging (i.e., fetching and
    storing) applications.

    Parameters
    ----------

    options_obj: object

        A Python object containing the attributes collect via the
        command line from the application driver script.

    Raises
    ------

    StagingError:

        * raised if a mandatory argument can not be determined from
          the specified command line options/attributes.

        * raised if the YAML-formatted configuration file, specified
          via the command line options/attributes, does not exist.

    """

    @classmethod
    def __init__(cls, options_obj: object, task_id: str = None):
        """
        Description
        -----------

        Creates a new Staging object.

        """

        # Define the base-class attributes.
        self = cls
        self.options_obj = options_obj
        self.logger = Logger()
        self.launch = Launch(options_obj=self.options_obj, task_id=task_id)
        self.launch.build_dirpath()
        self.launch.build_configs()

        # Check that the mandatory arguments have been provided within
        # the options_obj parameter; proceed accordingly.
        mand_args_list = ["cycle", "yaml_file"]

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
        self.yaml_dict = YAML().read_concat_yaml(
            yaml_file=self.yaml_file, return_obj=False
        )

    def _nc_concat(self, fileid_obj: object, fileconcat_obj: object) -> None:
        """
        Description
        -----------

        This method concatenates netCDF-formatted files in accordance
        with the respective file identifier attributes.

        Parameters
        ----------

        fileid_obj: object

            A Python object containing the attributes collected from
            the experiment configuration for the respective file
            identifier.

        fileconcat_obj: object

            A Python object containing the netCDF-formatted file
            concatentation attributes.

        Raises
        ------

        StagingError:

            * raised if a netCDF concatenation attribute is NoneType
              prior to the respective netCDF-formatted file
              concatenation.

        """

        # Define the list of files to be concatenated.
        ncfilelist = []
        for timestamp in fileid_obj.timestamps_list:

            # Define the netCDF-formatted file path.
            ncfile = datetime_interface.datestrupdate(
                datestr=str(timestamp),
                in_frmttyp=timestamp_interface.GLOBAL,
                out_frmttyp=fileid_obj.local_path,
            )

            # Check that the netCDF-formatted file path exists;
            # proceed accordingly.
            exist = fileio_interface.fileexist(path=ncfile)

            if exist:
                msg = (
                    f"The netCDF-formatted file path {ncfile} exists and "
                    "will be included in the netCDF file concatenation."
                )
                self.logger.info(msg=msg)
                ncfilelist.append(ncfile)

            if not exist:
                msg = (
                    f"The netCDF-formatted file path {ncfile} does not "
                    "exist and will not be included in the netCDF "
                    "file concatenation."
                )
                self.logger.warn(msg=msg)

        # Define the netCDF concatenation attributes to be
        # collected from the experiment configuration.
        ncconcat_attrs_dict = {"ncdim": numpy.nan, "ncfile": numpy.nan, "ncfrmt": None}

        ncconcat_obj = parser_interface.object_define()
        for (ncconcat_attr, _) in ncconcat_attrs_dict.items():

            # Collect the respective netCDF attribute; proceed
            # accordingly.
            value = parser_interface.dict_key_value(
                dict_in=fileconcat_obj.nc_concat,
                key=ncconcat_attr,
                force=True,
                no_split=True,
            )

            if value is None:

                # Check the valid values for the respective netCDF
                # attribute; proceed accordingly.
                check = parser_interface.dict_key_value(
                    dict_in=ncconcat_attrs_dict, key=ncconcat_attr, no_split=True
                )

                if check == numpy.nan:
                    msg = (
                        "For netCDF-formatted file concatenation, the "
                        f"attribute {ncconcat_attr} cannot be NoneType. "
                        "Aborting!!!"
                    )
                    error(msg=msg)

            # Update the attribute value; proceed accordingly.
            try:
                value = datetime_interface.datestrupdate(
                    datestr=str(self.cycle),
                    in_frmttyp=timestamp_interface.GLOBAL,
                    out_frmttyp=value,
                    offset_seconds=fileid_obj.offset_seconds,
                )

            except TypeError:
                pass

            ncconcat_obj = parser_interface.object_setattr(
                object_in=ncconcat_obj, key=ncconcat_attr, value=value
            )

        # Check that netCDF-formatted member files exist; proceed accordingly.
        if (
            sum(fileio_interface.fileexist(path=filename) for filename in ncfilelist)
            > 0
        ):

            # Check that the directory tree corresponding to the
            # concatenated output file exists; proceed accordingly.
            fileio_interface.dirpath_tree(path=os.path.dirname(ncconcat_obj.ncfile))

            # Concatenate the respective files to the specified output
            # file path.
            netcdf4_interface.ncconcat(
                ncfilelist=ncfilelist,
                ncfile=ncconcat_obj.ncfile,
                ncdim=ncconcat_obj.ncdim,
                ncfrmt=ncconcat_obj.ncfrmt,
            )

        else:

            msg = (
                f"No netCDF files within list {ncfilelist} exist; netCDF-formatted "
                f"file path {ncconcat_obj.ncfile} will not be created."
            )
            self.logger.warn(msg=msg)

    def awss3_fetch(
        self,
        fileid_obj: object,
        checksum_filepath: str = None,
        checksum_index: bool = False,
        checksum_level: str = "md5",
    ) -> None:
        """
        Description
        -----------

        This method collects (i.e., fetches) a specified Amazon Web
        Services (AWS) s3 object path from a specified AWS s3 bucket;
        this method accepts an Python dictionary parameter containing
        the attributes required to correctly collect the specified AWS
        s3 bucket and object path file.

        Parameters
        ----------

        fileid_obj: object

            A Python object containing the attributes collected from
            the experiment configuration for the respective file
            identifier.

        Keywords
        --------

        checksum_filepath: str, optional

            A Python string specifying the path to the file containing
            the checksum hash index values for specified local file
            paths.

        checksum_index: bool, optional

            A Python boolean valued variable specifying whether to
            define checksum hash indices for each local file collected
            from the specified AWS s3 bucket and object path.

        checksum_level: str, optional

            A Python string specifying the hash index level (e.g.,
            type) for the respective AWS s3 collected files.

        Raises
        ------

        StagingError:

            * raised if the timestamp list cannot be determined for
              the respective file identifier object (see fileid_obj
              above) provided upon entry.

        """

        # Define the timestamp strings for the respective file
        # identifier.
        timestamps_list = parser_interface.object_getattr(
            object_in=fileid_obj, key="timestamps_list", force=True
        )

        if timestamps_list is None:
            msg = (
                "The attribute timestamps_list could not be determined "
                "from the specified file identifier object. Aborting!!!"
            )
            error(msg=msg)

        # Loop through each specified time and determine whether the
        # request AWS s3 bucket and object path exists; if so, update
        # the local Python list containing the files to be collected.
        aws_filelist = []
        for timestamp in timestamps_list:

            # Collect the file list using boto3 for the respective
            # object path.
            msg = f"Collecting filelist for timestamp {timestamp}."
            self.logger.info(msg=msg)

            boto3_filelist = boto3_interface.filelist(
                bucket=fileid_obj.bucket,
                object_path=datetime_interface.datestrupdate(
                    datestr=timestamp,
                    in_frmttyp=timestamp_interface.GLOBAL,
                    out_frmttyp=fileid_obj.object_path,
                ),
            )

            # Update the local Python list containing the files to be
            # collected.
            for boto3_file in boto3_filelist:
                aws_filelist.append(boto3_file)

        # Maintain only unique file names.
        aws_filelist = list(set(aws_filelist))
        if aws_filelist:
            msg = (
                "The following files were found within the AWS resource bucket "
                f"{fileid_obj.bucket}: {aws_filelist}."
            )
            self.logger.info(msg=msg)

        if not aws_filelist:
            msg = f"No files were found in AWS resource bucket {fileid_obj.bucket}."

        # Loop through each specified time; if the specified object
        # path exists, collect the respective file; proceed
        # accordingly.
        for timestamp in timestamps_list:

            # Define the respective file path names in accordance with
            # the respective timestamp; check that the directory tree
            # for the local filename exists.
            local_path = datetime_interface.datestrupdate(
                datestr=timestamp,
                in_frmttyp=timestamp_interface.GLOBAL,
                out_frmttyp=fileid_obj.local_path,
            )
            object_path = datetime_interface.datestrupdate(
                datestr=timestamp,
                in_frmttyp=timestamp_interface.GLOBAL,
                out_frmttyp=fileid_obj.object_path,
            )

            # Check that the respective object path exists in the AWS
            # resource bucket; proceed accordingly.
            if object_path in aws_filelist:

                # Check that the directory tree exists; proceed
                # accordingly.
                fileio_interface.dirpath_tree(path=os.path.dirname(local_path))

                # Collect the file from the specified AWS resource
                # bucket and object path and stage it locally.
                filedict = {local_path: object_path}

                boto3_interface.get(
                    bucket=fileid_obj.bucket,
                    filedict=filedict,
                    profile_name=fileid_obj.profile_name,
                )

                # Define the checksum index value for the collected
                # file.
                if checksum_index:

                    hash_index = self.get_hash_index(
                        filepath=local_path, hash_level=checksum_level
                    )
                    msg = f"The hash index for file path {local_path} is {hash_index}."
                    self.logger.warn(msg=msg)

                # Check the checksum index writing parameter value and
                # proceed accordingly.
                if checksum_index and checksum_filepath is not None:

                    # Write the checksum index value to the specified
                    # external file path.
                    self.write_fetch_checksum(
                        checksum_filepath=checksum_filepath,
                        local_path=local_path,
                        hash_index=hash_index,
                    )

    def build_fileid_obj(
        self,
        filesdict: dict,
        fileid: str,
        mand_attr_list: list = None,
        opt_attr_dict: dict = None,
    ) -> object:
        """
        Description
        -----------

        This method builds a Python object containing the attributes
        gathered from the YAML-formatted configuration file for the
        specified file identifier; refer to the top-level README for
        additional information.

        Parameters
        ----------

        filesdict: dict

            A Python dictionary containing the local and remote paths
            for the files to be collected; the Python dictionary keys
            are the local host path(s) for the collected files while
            the Python dictionary values are the corresponding remote
            host file paths.

        fileid: str

            A Python string specifying the file identifier; this is a
            respective key in the respective YAML-formatted
            configuration file.

        Keywords
        --------

        mand_attr_list: list, optional

            A Python list containing the mandatory attributes to be
            collected for the respective file identifier from the
            YAML-formatted configuration file.

        opt_attr_dict: dict, optional

            A Python dictionary containing optional attributes and
            corresponding default value for the respective file
            identifier from the YAML-formatted configuration file.

        Returns
        -------

        fileid_obj: object

            A Python object containing the attributes collected from
            the experiment configuration for the respective file
            identifier.

        """

        # Define the attributes for the respective file identifier.
        fileid_obj = parser_interface.object_define()
        fileid_attrs = parser_interface.dict_key_value(
            dict_in=filesdict, key=fileid, no_split=True
        )

        # Define the optional Python object attributes for the
        # respective interface fetch method; proceed accordingly.
        if opt_attr_dict is not None:

            for opt_attr in opt_attr_dict.keys():

                value = parser_interface.dict_key_value(
                    dict_in=fileid_attrs, key=opt_attr, force=True, no_split=True
                )

                if value is None:

                    # Assign the default value for the respective
                    # attribute.
                    attr_value = parser_interface.dict_key_value(
                        dict_in=opt_attr_dict, key=opt_attr, no_split=True
                    )

                    msg = (
                        f"The attribute {opt_attr} for file identifier "
                        f"{fileid} could not be determined from the "
                        "YAML-formatted configuration file; setting to "
                        f"default value {attr_value}."
                    )
                    self.logger.warn(msg=msg)

                if value is not None:
                    attr_value = value
                    msg = (
                        f"The attribute {opt_attr} for file identifier "
                        f"{fileid} has value {attr_value}."
                    )
                    self.logger.info(msg=msg)

                # Define the respective Python object attribute.
                fileid_obj = parser_interface.object_setattr(
                    object_in=fileid_obj, key=opt_attr, value=attr_value
                )

        # Define the mandatory Python object attributes for the
        # respective interface fetch method; proceed accordingly.
        if mand_attr_list is not None:

            for mand_attr in mand_attr_list:

                # Define the mandatory attribute value; proceed
                # accordingly.
                value = parser_interface.dict_key_value(
                    dict_in=fileid_attrs, key=mand_attr, force=True, no_split=True
                )

                if value is None:
                    msg = (
                        f"The mandatory attribute {mand_attr} could not "
                        f"be determined for file identifier {fileid}. "
                        "Aborting!!!"
                    )
                    error(msg=msg)

                # Define the respective Python object attribute.
                fileid_obj = parser_interface.object_setattr(
                    object_in=fileid_obj, key=mand_attr, value=value
                )

        return fileid_obj

    def concat_filepath(self, fileid_obj: object) -> None:
        """
        Description
        -----------

        This method concatenates local host file paths in accordance
        with the specifications within the experiment configuration
        file.

        Parameters
        ----------

        fileid_obj: object

            A Python object containing the attributes collected from
            the experiment configuration for the respective file
            identifier.

        Raises
        ------

        StagingError:

            * raised if multiple file type concatenations have been
              specified upon entry (i.e., nc_concat, binary_concat,
              etc.,).

        """

        # Define the file manipulation options.
        fileid_concat_type_list = ["bufr_concat", "nc_concat"]

        # Define the file concatenation/manipulation options in
        # accordance with the experiment configuration.
        fileconcat_obj = parser_interface.object_define()

        for fileid_concat_type in fileid_concat_type_list:
            value = parser_interface.object_getattr(
                object_in=fileid_obj, key=fileid_concat_type, force=True
            )

            fileconcat_obj = parser_interface.object_setattr(
                object_in=fileconcat_obj, key=fileid_concat_type, value=value
            )

        # Define the file concatenation/manipulation type; proceed
        # accordingly.
        fileid_concat_types = [
            concat_type
            for concat_type in fileid_concat_type_list
            if parser_interface.object_getattr(
                object_in=fileconcat_obj, key=concat_type, force=True
            )
            is not None
        ]

        if len(fileid_concat_types) <= 0:
            msg = (
                "No file concatenation type has been specified "
                "for the respective file identifier; nothing "
                "will be done."
            )
            self.logger.warn(msg=msg)
            return

        if len(fileid_concat_types) > 1:
            msg = (
                "Multiple file concatenation types have been "
                "specified; only one concatenation type is "
                "supported for a respective file identifier; "
                "Aborting!!!"
            )
            error(msg=msg)

        # Concatenate the local file paths in accordance with the file
        # identifier object upon entry.
        concat_type = fileid_concat_types[0]

        if str(concat_type).lower() == "nc_concat":

            # Concatenate the respective netCDF-formatted file.
            self._nc_concat(fileid_obj=fileid_obj, fileconcat_obj=fileconcat_obj)

    def get_hash_index(self, filepath: str, hash_level: str = None) -> str:
        """
        Description
        -----------

        This method defines a checksum hash index value for the
        specified(local) file path.

        Parameters
        ----------

        filepath: str

            A Python string specifying the local file path for the
            file for which to define the checksum hash index value.

        Keywords
        --------

        hash_level: str, optional

            A Python string specifying the hash level for the
            respective hash index; currently supported values are md5,
            new, pbkdf2_hmac, sha1, sha224, sha256, sha384, and
            sha512; if NoneType, the md5 hash level is assumed.

        Returns
        -------

        hash_index: str

            A Python string containing the hash index for the user
            specified file path.

        """

        # Define the hash index value for the specified local file
        # path; proceed accordingly.
        try:
            hash_index = hashlib_interface.get_hash(
                filepath=filepath, hash_level=hash_level
            )

        except FileNotFoundError:
            msg = (
                f"File path {filepath} does not exist and therefore no checksum "
                "hash index value will be computed."
            )
            self.logger.warn(msg=msg)
            hash_index = None

        return hash_index

    def get_timestamps_list(self, fileid_obj: object) -> object:
        """
        Description
        -----------

        This method defines a list of timestamp strings in accordance
        with the respective file identifier attributes.

        Parameters
        ----------

        fileid_obj: object

            A Python object containing the attributes collected from
            the experiment configuration for the respective file
            identifier.

        Returns
        -------

        fileid_out_obj: object

            A deep copy of the Python obect containing the file
            identifier attributes and now including a list of strings
            specifying the timestamps corresponding to the attributes
            specified within the experiment configuration for the
            respective file identifier; the Python object key is
            timestamps_list.

        Raises
        ------

        StagingError:

            * raised if a value for a mandatory multiple file
              attribute is NoneType upon entry.

            * raised if the multiple file attribute offset_seconds is
              less than or equal to zero upon entry.

        """

        # If multiple files are to be collected for a specific
        # application, proceed accordingly.
        multifile_dict = parser_interface.object_getattr(
            object_in=fileid_obj, key="multifile", force=True
        )

        # Build a list of timestamps in accordance with the experiment
        # configuration.
        timestamps_list = []
        if multifile_dict is None:

            # Define a list of timestamps containing only the
            # respective analysis cycle.
            timestamp = datetime_interface.datestrupdate(
                datestr=str(self.cycle),
                in_frmttyp=timestamp_interface.GLOBAL,
                out_frmttyp=timestamp_interface.GLOBAL,
                offset_seconds=fileid_obj.offset_seconds,
            )

            timestamps_list.append(timestamp)

        if multifile_dict is not None:

            # Collect the multiple file attributes from the experiment
            # configuration.
            multifile_attrs_list = [
                "offset_seconds",
                "start_offset_seconds",
                "stop_offset_seconds",
            ]

            multifile_obj = parser_interface.object_define()
            for multifile_attr in multifile_attrs_list:

                # Collect the multiple file attribute; proceed
                # accordingly.
                value = parser_interface.dict_key_value(
                    dict_in=multifile_dict,
                    key=multifile_attr,
                    force=True,
                    no_split=True,
                )
                if value is None:
                    msg = (
                        "For multiple file collections the multifile "
                        f"attribute {multifile_attr} cannot be NoneType. "
                        "Aborting!!!"
                    )
                    error(msg=msg)

                multifile_obj = parser_interface.object_setattr(
                    object_in=multifile_obj, key=multifile_attr, value=value
                )

            # Check that the experiment configuration values are
            # valid; proceed accordingly.
            if multifile_obj.offset_seconds <= 0:
                msg = (
                    "For collecting multiple files the attribute "
                    "offset_seconds cannot be less than or equal to "
                    f"zero; received {multifile_obj.offset_seconds} "
                    "upon entry. Aborting!!!"
                )
                error(msg=msg)

            # Define the beginning of the timestamp window.
            offset_seconds = (
                fileid_obj.offset_seconds + multifile_obj.start_offset_seconds
            )
            start_timestamp = datetime_interface.datestrupdate(
                datestr=str(self.cycle),
                in_frmttyp=timestamp_interface.GLOBAL,
                out_frmttyp=timestamp_interface.GLOBAL,
                offset_seconds=offset_seconds,
            )

            # Define end of the timestamp window.
            offset_seconds = (
                fileid_obj.offset_seconds + multifile_obj.stop_offset_seconds
            )
            stop_timestamp = datetime_interface.datestrupdate(
                datestr=str(self.cycle),
                in_frmttyp=timestamp_interface.GLOBAL,
                out_frmttyp=timestamp_interface.GLOBAL,
                offset_seconds=offset_seconds,
            )

            # Build a list of timestamps within the specified window;
            # proceed accordingly.
            timestamp = start_timestamp
            while timestamp <= stop_timestamp:

                # Update the current timestamp relative to the
                # specified interval.
                timestamps_list.append(timestamp)

                timestamp = datetime_interface.datestrupdate(
                    datestr=str(timestamp),
                    in_frmttyp=timestamp_interface.GLOBAL,
                    out_frmttyp=timestamp_interface.GLOBAL,
                    offset_seconds=multifile_obj.offset_seconds,
                )

            timestamps_list = sorted(list(set(timestamps_list)))

        # For each timestamp, check that the timestamps are valid;
        # proceed accordingly.
        timestamps_list_check = timestamps_list
        for timestamp in timestamps_list:

            # If the timestamp is outside of the specified stream
            # start and stop timestamps, proceed accordingly.
            if (int(timestamp) < int(fileid_obj.stream_start)) or (
                int(timestamp) > int(fileid_obj.stream_stop)
            ):

                # Remove the respective timestamp from the list.
                msg = (
                    f"The timestamp {timestamp} is not within the specified "
                    f"stream range {fileid_obj.stream_start} and "
                    f"{fileid_obj.stream_stop} and will not be "
                    "included/retrieved."
                )
                self.logger.warn(msg=msg)
                timestamps_list_check.remove(timestamp)

            else:

                msg = (
                    f"The timestamp {timestamp} is within the specified "
                    "stream range and will be collected."
                )
                self.logger.info(msg=msg)

        # Update the file identifier object.
        fileid_out_obj = parser_interface.object_deepcopy(object_in=fileid_obj)
        fileid_out_obj = parser_interface.object_setattr(
            object_in=fileid_out_obj, key="timestamps_list", value=timestamps_list
        )

        return fileid_out_obj

    def write_fetch_checksum(
        self, checksum_filepath: str, local_path: str, hash_index: str
    ) -> None:
        """
        Description
        -----------

        This method writes the checksum hash index value for the
        respective local file path to the file path, specified upon
        entry, to contain the respective checksum hash index values;
        if hash_index is NoneType upon entry, the respective hash
        index will not be written to the specified file path.

        Parameters
        ----------

        checksum_filepath: str

            A Python string specifying the path to the file containing
            the checksum hash index values for specified local file
            paths.

        local_path: str

            A Python string specifying the path to the local file for
            which the respective checksum hash index value was
            defined.

        hash_index: str

            A Python string containing the hash index for the local
            file path specified upon entry.

        """

        # Write the checksum hash index value to the specified file
        # path; proceed accordingly.
        if hash_index is not None:

            fileio_interface.dirpath_tree(path=os.path.dirname(checksum_filepath))

            with open(checksum_filepath, "a", encoding="utf-8") as file:
                file.write(f"{hash_index} {local_path}\n")


# ----


@msg_except_handle(StagingError)
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
