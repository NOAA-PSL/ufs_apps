# Unified Forecast System Workflow Staging Configurations

The Unified Forecast System (UFS) workflow staging applies to the
fetching (i.e., collecting) and storing (i.e., saving) of specified
files. This README provides a description of the available
YAML-formatted configuration options.

## Fetching Application Configuration

Yhe following YAML snippet provides an example YAML-formatted
configuration file for fetching user-specified files.

~~~
fetch:

     checksum:

          <CHECKSUM ATTRIBUTES>

     interface_platform:

          fetching_option:

               file_identifier:

                    <FILE IDENTIFIER ATTRIBUTES>
~~~
