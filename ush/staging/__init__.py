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

"""

# ----

import numpy
import os

from ioapps import boto3_interface
from ioapps import hashlib_interface
from ioapps import netcdf4_interface
from tools import datetime_interface
from tools import fileio_interface
from tools import parser_interface
from utils import timestamp_interface
from utils.error_interface import Error
from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class Staging():
    """

    """

    def __init__(self, options_obj: object):
        """
        Description
        -----------

        Creates a new Staging object.

        """

        # Define the base-class attributes.
        self.options_obj = options_obj
        self.logger = Logger()

        # Check that the mandatory arguments have been provided within
        # the options_obj parameter; proceed accordingly.
        mand_args_list = ['cycle',
                          'yaml_file'
                          ]

        for mand_arg in mand_args_list:

            # Check that the mandatory argument has been provided;
            # proceed accordingly.
            value = parser_interface.object_getattr(
                object_in=self.options_obj, key=mand_arg, force=True)

            if value is None:
                msg = ('The option attributes provided to the base-class does not '
                       f'contain the mandatory attribute {mand_arg}. Aborting!!!')
                raise StagingError(msg=msg)

            # Update the base-class object attribute.
            self = parser_interface.object_setattr(object_in=self,
                                                   key=mand_arg, value=value)

        # Check that the timestamp string is of the correct format;
        # proceed accordingly.
        timestamp_interface.check_frmt(
            datestr=self.cycle, in_frmttyp=timestamp_interface.GLOBAL,
            out_frmttyp=timestamp_interface.GLOBAL)

        # Check that the YAML-formatted configuration file exists;
        # proceed accordingly.
        exist = fileio_interface.fileexist(path=self.yaml_file)

        if not exist:
            msg = (f'The YAML-formatted configuration file {self.yaml_file} '
                   'does not exist. Aborting!!!')
            raise StagingError(msg=msg)

        # Parse the configuration file.
        self.yaml_dict = fileio_interface.read_yaml(yaml_file=self.yaml_file)

    def awss3_fetch(self, fileid_obj: object, checksum_filepath: str = None,
                    checksum_index: bool = False,
                    checksum_level: str = 'md5') -> None:
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
            object_in=fileid_obj, key='timestamps_list', force=True)

        if timestamps_list is None:
            msg = ('The attribute timestamps_list could not be determined '
                   'from the specified file identifier object. Aborting!!!')
            raise StagingError(msg=msg)

        # Loop through each specified time and proceed accordingly.
        for timestamp in timestamps_list:

            # Define the respective file path names in accordance with
            # the respective timestamp; check that the directory tree
            # for the local filename exists; proceed accordingly.
            local_path = datetime_interface.datestrupdate(
                datestr=timestamp, in_frmttyp=self.cyclestr_frmt,
                out_frmttyp=fileid_obj.local_path)
            object_path = datetime_interface.datestrupdate(
                datestr=timestamp, in_frmttyp=self.cyclestr_frmt,
                out_frmttyp=fileid_obj.object_path)

            self.build_dirpath_tree(path=os.path.dirname(local_path))

            # Collect the file from the specified AWS s3 bucket and
            # object path and stage it locally.
            filedict = {local_path: object_path
                        }
            boto3_interface.s3get(
                bucket=fileid_obj.bucket, filedict=filedict,
                profile_name=fileid_obj.profile_name)

            # Define the checksum index value for the collected file.
            if checksum_index:

                hash_index = self.get_hash_index(filepath=local_path,
                                                 hash_level=checksum_level)
                msg = ('The hash index for file path {0} is {1}.'.format(
                    local_path, hash_index))
                self.logger.warn(msg=msg)

            # Check the checksum index writing parameter value and
            # proceed accordingly.
            if checksum_index and checksum_filepath is not None:

                # Write the checksum index value to the specified
                # external file path.
                self.write_fetch_checksum(
                    checksum_filepath=checksum_filepath, local_path=local_path,
                    hash_index=hash_index)

    def build_dirpath_tree(self, path: str) -> None:
        """
        Description
        -----------

        This method checks whether the directory tree (i.e., path)
        exists; if not an attempt will be made to build it.

        Parameters
        ----------

        path: str

            A Python string specifying the directory tree path to be
            created if it does not (yet) exist.

        Raises
        ------

        StagingError:

            * raised if an exception is encountered while attempting
              to build the specified directory tree.

        """

        # Check whether the directory tree exists; proceed
        # accordingly.
        exist = fileio_interface.fileexist(path=path)
        if exist:
            msg = ('The directory tree {0} exists; nothing to be done.'
                   .format(path))
            self.logger.info(msg=msg)

        if not exist:
            msg = ('The directory tree {0} does not exist; an attempt '
                   'will be made to create it.'.format(path))
            self.logger.warn(msg=msg)

            try:
                fileio_interface.makedirs(path=path)

            except Exception as error:
                msg = ('Creating directory tree {0} failed with error '
                       '{1}. Aborting!!!'.format(path, error))
                raise StagingError(msg=msg)


# ----

class StagingError(Error):
    """
    Description
    -----------

    This is the base-class for all exceptions; it is a sub-class of
    Error.

    Parameters
    ----------

    msg: str

        A Python string to accompany the raised exception.

    """

    def __init__(self, msg: str):
        """
        Description
        -----------

        Creates a new StagingError object.

        """
        super(StagingError, self).__init__(msg=msg)
