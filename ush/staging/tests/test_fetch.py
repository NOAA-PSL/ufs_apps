# =========================================================================

# Module: staging/tests/test_fetch.py

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

    test_fetch.py

Description
-----------

    This module provides unit-test for the respective fetch
    application capabilities.

Classes
-------

    TestFetchMethods()

        This is the base-class object for all fetch application
        unit-tests; it is a sub-class of TestCase.

Requirements
------------

- boto3; https://github.com/boto/boto3

- moto; https://github.com/spulec/moto

- pytest; https://docs.pytest.org/en/7.2.x/

- pytest-order; https://github.com/pytest-dev/pytest-order

Author(s)
---------

    Henry R. Winterbottom; 04 January 2023

History
-------

    2023-01-04: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=undefined-variable

# ----

import os
from unittest import TestCase

import boto3
import pytest
from confs.yaml_interface import YAML
from moto import mock_s3
from staging.fetch import Fetch
from tools import fileio_interface, parser_interface

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Define the generic unit-test attributes for the fetch application.
CYCLE = "20000101000000"
YAML_FILE = "test_fetch.yaml"

# Define the AWS s3 fetch application unit-test attributes.
AWSS3_REGION = "us-east-1"
AWSS3_TEST_MESSAGE = "UNIT TEST FOR FETCH APPLICATION AWS S3 INTERFACE"

# ----


class TestFetchMethods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all fetch application
    unit-tests; it is a sub-class of TestCase.

    """

    def setUp(self):
        """
        Description
        -----------

        This method defines the base-class attributes for all
        fetch application unit-tests.

        """

        # Define base-class attributes.
        self.dirpath = os.getcwd()
        self.yaml_file = os.path.join(self.dirpath, "test_files", YAML_FILE)
        self.cycle = CYCLE

        # Collect the unit-test attributes from the YAML-formatted
        # file.
        self.yaml_dict = YAML().read_yaml(yaml_file=self.yaml_file)["fetch"]

    def build_options_obj(self, platform: str) -> object:
        """
        Description
        -----------

        This method builds the Python object options attributes and
        initializes and returns the fetching application interface for
        the respective platform/interface type.

        Parameters
        ----------

        platform: str

            A Python string specifying the platform/interface type.

        Returns
        -------

        fetch: object

            A Python object containing the fetching application
            interface for the respective platform/interface type.

        """

        # Initialize the Python object to contain the options for the
        # fetch application.
        options_obj = parser_interface.object_define()

        # Create the options Python object and initialize the fetch
        # application.
        options_obj = parser_interface.object_setattr(
            object_in=options_obj, key="cycle", value=self.cycle
        )
        options_obj = parser_interface.object_setattr(
            object_in=options_obj, key="yaml_file", value=self.yaml_file
        )
        options_obj = parser_interface.object_setattr(
            object_in=options_obj, key="platform", value=platform
        )

        # Initialize the fetch application.
        fetch = Fetch(options_obj=options_obj)

        return fetch

    def cleanup(self, filelist: list) -> None:
        """
        Description
        -----------

        This method removes the specified no-longer necessary
        unit-test files.

        Parameters
        ----------

        filelist: list

            A Python list contianing the no-longer necessary unit-test
            files to be removed.

        """

        # Remove the specified files.
        fileio_interface.removefiles(filelist=filelist)

    @pytest.mark.order(1)
    @mock_s3
    def test_fetch_awss3(self) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the fetch application AWS
        s3 platform/interface.

        """

        # Define the platform/interface against which to test the
        # fetch application.
        platform = "aws_s3"
        fetch = self.build_options_obj(platform=platform)

        # Collect the relevant YAML-formatted key and value pairs.
        awss3_test_dict = self.yaml_dict[platform]["test_awss3"]["test_awss3_file"]

        # Build a local Python object containing the attributes for
        # the local AWS s3 emulator.
        mock_obj = parser_interface.object_define()
        mock_list = ["bucket", "local_path", "object_path"]

        for mock_item in mock_list:

            # Define the Python object attributes.
            value = parser_interface.dict_key_value(
                dict_in=awss3_test_dict, key=mock_item, no_split=True
            )
            mock_obj = parser_interface.object_setattr(
                object_in=mock_obj, key=mock_item, value=value
            )

        # Create a mock AWS s3 bucket.
        conn = boto3.resource("s3", region_name=AWSS3_REGION)
        conn.create_bucket(Bucket=mock_obj.bucket)

        # Create the mock AWS s3 bucket object path.
        awss3 = boto3.client("s3", region_name=AWSS3_REGION)
        awss3.put_object(
            Bucket=mock_obj.bucket, Key=mock_obj.object_path, Body=AWSS3_TEST_MESSAGE
        )

        # Collect the attribute from the specified AWS s3 bucket
        # object path.
        fetch.run()

        assert True

        # Check that the contents of the collected file are valid.
        with open(awss3_test_dict["local_path"], "r", encoding="utf-8") as file:
            data = file.read()

        assert data == AWSS3_TEST_MESSAGE

        # Define and remove the test files.
        filelist = []
        filelist.append(awss3_test_dict["local_path"])
        self.cleanup(filelist=filelist)


# ----

if __name__ == "__main__":
    unittest.main()
