### UFS Ocean Observation Fetch Application Configurations[^1]

<div align="center">

| Configuration | Description |
| :-------------: | :-------------: |
| [`fetch.adt.reanalysis.yaml`](fetch.adt.reanalysis.yaml) | <div align="left">UFS reanalysis project ocean absolute dynamic topography observations. </div>|
| [`fetch.insitu.reanalysis.yaml`](fetch.insitu.reanalysis.yaml) | <div align="left">UFS reanalysis project ocean insitu observations. </div>|
| [`fetch.sst.reanalysis.yaml`](fetch.sst.reanalysis.yaml) | <div align="left">UFS reanalysis project ocean sea-surface salinity observations. </div>|
| [`fetch.sst.reanalysis.yaml`](fetch.sst.reanalysis.yaml) | <div align="left">UFS reanalysis project ocean sea-surface temperature observations. </div>|

</div>

[^1]: The ocean observations for the UFS reanalysis, with the exception of SST, are collected from the [JCSDA](https://www.jcsda.org/) [SOCA-science](https://github.com/jcsda-internal/soca-science) [NG-GODAS](https://tinyurl.com/SOCA-NGGODAS) experiment. For the respective experiments observations are assimilated every 24-hours and assuming the observations centered at 1200 UTC for the respective day. The time-stamps within the respective YAML-formatted configuration files have been defined such that the 1200 UTC-centered observations are collected for each ice analysis time such that the data-assimilation application is able to parse and use the available observations.

#

Please direct questions to [Henry
R. Winterbottom](mailto:henry.winterbottom@noaa.gov?subject=[UFS-Applications])