[![License](https://img.shields.io/badge/license-LGPL_v2.1-black)](https://github.com/HenryWinterbottom-NOAA/ufs_apps/blob/develop/LICENSE)
![Linux](https://img.shields.io/badge/linux-ubuntu%7Ccentos-lightgrey)
![Python Version](https://img.shields.io/badge/python-3.5|3.6|3.7-blue)

[![Dependencies](https://img.shields.io/badge/dependencies-ufs__pyutils-orange)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils)


[![Unit Tests](https://github.com/HenryWinterbottom-NOAA/ufs_apps/actions/workflows/unittests.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_apps/actions/workflows/unittests.yaml)
[![Python Coding Standards](https://github.com/HenryWinterbottom-NOAA/ufs_apps/actions/workflows/pycodestyle.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_apps/actions/workflows/pycodestyle.yaml)
[![Container Builds](https://github.com/HenryWinterbottom-NOAA/ufs_apps/actions/workflows/containers.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_apps/actions/workflows/containers.yaml)

# Disclaimer

The United States Department of Commerce (DOC) GitHub project code is
provided on an "as is" basis and the user assumes responsibility for
its use. DOC has relinquished control of the information and no longer
has responsibility to protect the integrity, confidentiality, or
availability of the information. Any claims against the Department of
Commerce stemming from the use of its GitHub project will be governed
by all applicable Federal law. Any reference to specific commercial
products, processes, or services by service mark, trademark,
manufacturer, or otherwise, does not constitute or imply their
endorsement, recommendation or favoring by the Department of
Commerce. The Department of Commerce seal and logo, or the seal and
logo of a DOC bureau, shall not be used in any manner to imply
endorsement of any commercial product or activity by DOC or the United
States Government.

# Supported Applications

The applications listed in the following table are (currently)
supported by the authoritative repository.

<div align="center">

| Application | Description |
| :-------------: | :-------------: |
| [Staging](parm/staging/README.md) | File fetching (i.e., collecting) and storing (i.e., saving) applications. | 


</div>

# Cloning

This repository utilizes several sub-modules from various sources. To
obtain the entire system, do as follows.

~~~
user@host:$ git clone --recursive https://github.com/HenryWinterbottom-NOAA/ufs_apps
~~~

# Forking

If a user wishes to contribute modifications done within their
respective fork(s) to the authoritative repository, we request that
the user first submit an issue and that the fork naming conventions
follow those listed below.

- `docs/user_fork_name`: Documentation additions and/or corrections for the UFS applications.

- `feature/user_fork_name`: Additions, enhancements, and/or upgrades for the UFS applications.

- `fix/user_fork_name`: Bug-type fixes for the UFS applications that do not require immediate attention.

- `hotfix/user_fork_name`: Bug-type fixes which require immediate attention to fix issues that compromise the integrity of the respective UFS applications. 
