### UFS Ice Observation Fetch Application Configurations

<div align="center">

| Configuration | Description |
| :-------------: | :-------------: |
| [`fetch.icec.reanalysis.yaml`](fetch.icec.reanalysis.yaml)[^1] | <div align="left">UFS reanalysis project ice concentration observations. </div>|
| [`fetch.icefb.reanalysis.yaml`](fetch.icefb.reanalysis.yaml)[^1] | <div align="left">UFS reanalysis project ice thickness (freeboard) observations. </div>|

</div>

[^1]: The ice observations for the UFS reanalysis are collected from the [JCSDA](https://www.jcsda.org/) [SOCA-science](https://github.com/jcsda-internal/soca-science) [NG-GODAS](https://tinyurl.com/SOCA-NGGODAS) experiment when observations are assimilated every 24-hours and centered at 1200 UTC for the respective day. The time-stamps within the respective YAML-formatted configuration files have been defined such that the 1200 UTC-centered observations are collected for each ice analysis time such that the respective data-assimilation application is able to parse and use what respective observations are available.

#

Please direct questions to [Henry
R. Winterbottom](mailto:henry.winterbottom@noaa.gov?subject=[UFS-Applications])