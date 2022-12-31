# Experiment Configurations

The Unified Forecast System (UFS) workflow configuration requires
YAML-formatted configuration files specifying various YAML keys
relative to specific (available) applications. The YAML-formatted
configuration files may be created manually or using the tools
available from
[`ufs_pyutils`](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils). The
mandatory YAML key and value pairs that are required of all
applications are listed in the following table.

<div align="center">

| Attribute | Description |
| :-------------: | :-------------: |
| `coupled` | <div align="left">This is a Python boolean valued variable specifying whether the UFS application is a coupled model application. </div> | 
| `cycling` | <div align="left">This is a Python boolean valued variable specifying whether the UFS application is cycling (i.e., has previous forecast cycle dependencies). </div> | 
| `expt_yaml` | <div align="left">This is a Python string that defines the base-name to contain the experiment configuration attributes; this file will be written beneath the respective experiment/cycle /com and /intercom paths. </div> |

</div>

An example YAML-formatted configuration file is as follows.

~~~
# Experiment configuration.
coupled: True
cycling: True
expt_yaml: !ENV ufs.${EXPTufs}.${CYCLEufs}.yaml

# ----

# UFS application configuration files.
fetch: /path/to/fetch_config
stage: /path/to/stage_config
  .
  .
  .
~~~

Please direct questions to [Henry
R. Winterbottom](mailto:henry.winterbottom@noaa.gov?subject=[UFS-Applications])