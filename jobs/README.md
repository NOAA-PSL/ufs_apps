# Job-Level Scripts

The Unified Forecast System (UFS) workflow job-level scripts are
provided as an interface to the respective UFS workflow engine (e.g.,
Rocoto, Cylc, ecFlow, etc.,). Each job-level script requires run-time
environment variables to be specified such that each can launch and
execute it's respective task(s). The respective environment variables
common to each job-level script are listed in the following table.

<div align="center">

| Environment Variable | Description |
| :-------------: | :-------------: |
| `CYCLEufs` | <div align="left">The respective UFS forecast cycle; the format is `%Y%m%d%H%M%S` assuming the POSIX convention.</div> |
| `HOMEufs` | <div align="left">The top-level working directory for all UFS applications.</div> |
| `PREufs` | <div align="left">The full-path to the (supported) platform-dependent required utilities and/or modules script.</div> |
| `YAMLufs` | <div align="left">The YAML-formatted configuration file for the respective UFS experiment.</div> | 

</div>

The `PREufs` environment variable specifies the bash script for a
supported Linux platform which defines the run-time environment
instructions for each respective task. This script is typically found
beneath the [UFS applications](https://github.com/HenryWinterbottom-NOAA/ufs_apps) `modulefiles` path. The environment variables
corresponding to the run-time environment to be loaded for a
respective job-level script/task are provided in the following table.

<div align="center">

| Environment Variable | Description |
| :-------------: | :-------------: |
| `UFS_STAGE=1` | <div align="left">Load all run-time modules for staging (e.g., fetching and storing) remotely or locally hosted files required for a UFS experiment. </div> | 

</div>

The job-level scripts for various UFS experiment applications and
configurations are provided within the sub-directories described in
the following table.

<div align="center">

| Subdirectory | Description |
| :-------------: | :-------------: |
| `reanalysis` | <div align="left">UFS reanalysis experiment(s) applications. </div> |

</div>