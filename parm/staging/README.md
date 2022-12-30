# Staging Applications

The Unified Forecast System (UFS) workflow staging applies to the
fetching (i.e., collecting) and storing (i.e., saving) of specified
files. This README provides a description of the available
YAML-formatted configuration file options.

Note that the respective fetching and storing applications may rely on
external platform interfaces (e.g., [Amazon Web
Services](https://aws.amazon.com/), [Globus](https://www.globus.org/))
in order to collect and/or store specified file objects. As a result,
latency may be introduced via load on the aforementioned provider
platform interfaces and may slow performance. In order for users to
optimize performance for their respective applications, the following
sites should be consulted prior to launching a given staging
application.

- [Latency to the closest AWS region](https://docs.aws.amazon.com/whitepapers/latest/best-practices-deploying-amazon-workspaces/how-to-check-latency-to-the-closest-aws-region.html)
- [Global latency monitoring for all AWS regions](https://www.cloudping.co/grid/latency/timeframe/1D)

The relevant attributes for optimization are the respective AWS
regions. Performance can be optimized by choosing the AWS region
nearest to the request location with the lowest latency. Once a region
is chosen, the `region` attribute within the user `~/.aws/config`
corresponding to the respective profile should be updated. See
[updating AWS
configure](https://docs.aws.amazon.com/cli/latest/reference/configure/)
for additional information.

## Building a Fetching Application Configuration

The following YAML snippet provides an example architecture for the
YAML-formatted configuration files to be used for a UFS fetching
application. Descriptions for the respective attributes are provided
in the tables throughout this section.

~~~
# All attributes that follow are for the UFS fetching application.
fetch:

     # Define the checksum hash index attributes.
     checksum:
          .
	  .
          .

     # Define a supported the platform/interface from which to collect
     # the respective files.
     [interface_platform]:

          # Define the fetching type; this corresponds to ocean
          # observations.
          [fetching_option]:

	       # Define the file identifier.
	       [file_identifier]:
                    .
		    .
		    .
~~~

<div align="center">

| Attribute | Description |
| :-------------: | :-------------: |
| `fetch` | <div align="left">This attribute is mandatory for all fetching applications; this informs the application as to the relevant configuration attributes.</div> | 
| `checksum` | <div align="left">This optional attribute provides information relevant to the determination of checksum hash values for each file collected from the respective interface platform; a list of currently supported values can be found [here](#checksum-configuration-attributes).</div> |
| `[interface_platform]` | <div align="left">This value defines the interface platform from which to fetch files; the currently supported option is `aws_s3`.</div> |
| `[fetching_option]` | <div align="left">This value defines the file identifiers types to follow; as an example, for ocean or atmosphere type observation files, this attribute may read `ocean_obs` or `atmos_obs`, respectively; these attributes may also be used as optional command line arguments for the [fetching application script](https://github.com/HenryWinterbottom-NOAA/ufs_apps/blob/develop/scripts/exufs_fetch.py). </div> |
| `[file_identifier]` | <div align="left">This value assigns a unique name to the YAML key for which the attributes corresponding to the contents to be retrieved; for example, [National Environmental Satellite, Data, and Information Service (NESDIS)](https://www.nesdis.noaa.gov/) hosted observations for sea-surface temperature (SST) derived from the [AVHRR](https://www.eumetsat.int/avhrr) instrument onboard the National Oceanic and Atmospheric (NOAA) 15 satellite may have a file identifier such as `sst.nesdis_avhrr_noaa15`. </div> | 

</div>

### Checksum Configuration Attributes

<div align="center">

| Attribute | Description | Default Values | 
| :-------------: | :-------------: | :-------------: |
| `aws_s3_filepath` | <div align="left">The local file path to contain the checksum hash values for the AWS s3 interface platform downloaded files; environment variables and POSIX compliant time and date string attributes are supported when building this attribute</div> | None; if not provided the checksum hash values are written only to standard out. | 
| `aws_s3_hash` | <div align="left">The checksum hash types for the respective AWS s3 interface platform downloaded files; currently supported options are `md5`, `sha1`, `sha224`, `sha256`, `sha384`, and `sha512` </div> |  `md5` |

</div>

An example YAML-formatted configuration file using each of the
attributes defined above is as follows.

~~~
# All attributes that follow are for the UFS fetching application.
fetch:

     # Define the checksum hash index attributes.
     checksum:

       aws_s3_filepath: !ENV ${WORKufs}/${EXPTufs}/com/${CYCLEufs}/aws_s3.fetch.obs.md5     
       aws_s3_hash: md5
  
     # Define a supported the interface platform from which to collect
     # the respective files.
     aws_s3:	 

          # Define the fetching type; this example corresponds to
          # ocean observations.
	  ocean_obs:

	       # Define the file identifier.
               sst.nesdis_avhrr_noaa15:

                    # Define the attributes corresponding to the
                    # respective file identifier.
                    [file_identifier_attributes]
		         .
		         .
			 .
~~~

### File Identifier Attributes

The following tables provide the supported mandatory and optional file
identifier attributes.

<div align="center">

| Mandatory Attribute | Description | Platform/Interface | 
| :-------------: | :-------------: | :-------------: |
| `bucket` | <div align="left">The AWS s3 bucket from which collect the specified `object_path` (see below). | `aws_s3` | </div>
| `local_path` | <div align="left">The file path on the local host to where the fetched file will be staged; environment variables and POSIX compliant time and date string attributes are supported when building this attribute. | This value is required for all interface platforms. | </div>
| `object_path` | <div align="left">The AWS s3 object path beneath the AWS s3 `bucket` attribute defined above; environment variables and POSIX compliant time and date string attributes are supported when building this attribute.| `aws_s3` | </div> 
| `profile_name` | <div align="left">The AWS s3 profile to be used for AWS s3 interface platform file fetching; this value should be a profile name within the respective user `~/.aws/credentials` file path; if fetching from a public bucket this value should be set to `null`. | `aws_s3` | </div>

</div>

<div align="center">

| Optional Attribute | Description | Default Value | 
| :-------------: | :-------------: | :-------------: |
| `ignore_missing` | <div align="left">This is boolean value specifying whether to fail for missing platform/interface file paths (`False`) or to ignore a missing file and continue to process the attributes within the YAML-formatted configuration file (`True`). | `False` | </div>
| `multifile` |  <div align="left">See section [multifile configuration attributes](#multifile-configuration-attributes) below. | option is ignored | </div> 
| `nc_concat` | <div align="left">See section [netCDF concatenation configuration attributes](#netcdf-multifile-concatenation-attributes) below. | option is ignored | </div> |
| `offset_seconds` | <div align="left">The total number of offset seconds relative to the forecast date for valid files; this value is used to define any POSIX compliant time and date string information specified in `local_path`; this value is also used to build the `object_path` (see above). | `0` | </div>
| `stream_start` | <div align="left">The timestamp at which the respective datestream begins; format is `%Y%m%d%H%M%S` assuming the POSIX convention. | `19000101000000` | </div>
| `stream_stop` | <div align="left">The timestamp at which the respective datestream ends; format is `%Y%m%d%H%M%S` assuming the POSIX convention. | `20991231230000` | </div>

</div>

### Multifile Configuration Attributes

The following table provides the mandatory variables required to
collect multiple files for a given file identifier for the supported
platform/interface values.

<div align="center">

| Attribute | Description | 
| :-------------: | :-------------: |
| `offset_seconds` | <div align="left"> The total number of seconds specifying the interval at which to collect member files. </div> | 
| `start_offset_seconds` | <div align="left">The total number of seconds, prior to the respective forecast cycle timestamp, for which to begin collecting member files. </div> |
| `stop_offset_seconds` | <div align="left"> The total number of seconds, following the respective forecast cycle timestamp, for which to end collecting member files.</div> | 

</div>

### netCDF Multifile Concatenation Attributes

The following table provides the mandatory variables required to
concatenate [netCDF](https://www.unidata.ucar.edu/software/netcdf/)
formatted files for a given file identifier.

<div align="center">

| Attribute | Description | 
| :-------------: | :-------------: |
| `ncdim` | <div align="left">The netCDF dimension name along which to concatenate the respective member files.</div> |
| `ncfile` | <div align="left">The netCDF-formatted file path to contain the concatenated member files; environment variables and POSIX compliant time and date string attributes are supported when building this attribute.</div> |
| `ncfrmt` | <div align="left">The netCDF file format for the concatenated file path (see `ncfile`); supported values are `NETCDF3_CLASSIC`, `NETCDF3_64BIT_OFFSET`, `NETCDF3_64BIT_DATA`, `NETCDF4`, `NETCDF4_CLASSIC`. </div> | 
</div>

Using the attributes provided above, an example YAML-formatted
configuration file for a UFS fetching application is provided
below. This example assumes the following.

- The file identifier, as above, is `sst.nesdis_avhrr_noaa15`.

- A 6-hour timestamp relative to the respective forecast cycle.

- Hourly (i.e., multiple) netCDF-formatted files collected from an [AWS s3](https://aws.amazon.com/pm/serv-s3/?trk=fecf68c9-3874-4ae2-a7ed-72b6d19c8034&sc_channel=ps&s_kwcid=AL!4422!3!536452728638!e!!g!!aws%20s3&ef_id=Cj0KCQiA14WdBhD8ARIsANao07jcrgPFmsPPGxTJDSWizyp8U3k9WhPE95zHj5UNF2Jt8FdoJlMEoHMaAr7REALw_wcB:G:s&s_kwcid=AL!4422!3!536452728638!e!!g!!aws%20s3) relative to the specified forecast cycle. 

- Concatenation of the hourly netCDF-formatted member files along the `nlocs` netCDF dimension and formatted as `NETCDF4`.

~~~
# All attributes that follow are for the UFS fetching application.
fetch:

     # Define the checksum hash index attributes.
     checksum:

       aws_s3_filepath: !ENV ${WORKufs}/${EXPTufs}/com/${CYCLEufs}/aws_s3.fetch.obs.md5     
       aws_s3_hash: md5
  
     # Define a supported the interface platform from which to collect
     # the respective files.
     aws_s3:	 

          # Define the fetching type; this example corresponds to
          # ocean observations.
	  ocean_obs:

	       # Define the file identifier.
               sst.nesdis_avhrr_noaa15:

                    # Define the attributes corresponding to the
                    # respective file identifier.
		    local_path: !ENV ${WORKufs}/${EXPTufs}/${CYCLEufs}/intercom/obsprep/ocean/nesdis.avhrr_noaa15.sst.%Y%m%d.T%H%M%SZ.iodav2.so0p25.nc
		    offset_seconds: 21600

                    # Define the AWS s3 attributes for the respective
                    # file identifier.
                    bucket: noaa-reanalyses-pds
                    object_path: observations/reanalysis-test/sst/nesdis/avhrr/noaa15/%Y/%m/superob_0p25/iodav2/nesdis.avhrr_noaa15.sst.%Y%m%d.T%H%M%SZ.iodav2.so0p25.nc
                    profile_name: null
                    ignore_missing: True		    

                    # Define the attributes for multiple (i.e.,
                    # member file) collection applications; these are
                    # a single file containing all member files within
                    # the specified window.
		    multifile:

                         # Define the total number of seconds, prior
                         # to the relevant analysis timestamp, from
                         # which to begin collecting member files.
                         start_offset_seconds: -10800

                         # Define the total number of seconds,
                         # following the relevant the analysis timestamp,
                         # from which to end collecting member files.
                         stop_offset_seconds: 10800

                         # Define the total number of seconds
                         # specifying the interval at which to collect
                         # member files.
                         offset_seconds: 3600

                    # Define the netCDF-formatted member file
                    # concatenation attributes.
                    nc_concat:

                         # Define the dimension name along which to
                         # concatenate the respective member files.
                         ncdim: nlocs

                         # Define the netCDF-formatted file path to
                         # contain the results of the concatenated
                         # member files.
                         ncfile: !ENV ${WORKufs}/${EXPTufs}/${CYCLEufs}/intercom/inputs/obs/ocean/nesdis.avhrr_noaa15.sst.nc

                         # Define the netCDF-formatted concatenated
                         # file path format.
                         ncfrmt: NETCDF4
~~~

### Available Fetch Applications Configurations

<div align="center">

| Configuration | Description |
| :-------------: | :-------------: |
| [`fetch.adt.reanalysis.yaml`](fetch.adt.reanalysis.yaml) | <div align="left">UFS reanalysis project ocean absolute dynamic topography observations. </div>|
| [`fetch.airs.reanalysis.yaml`](fetch.airs.reanalysis.yaml) | <div align="left">UFS reanalysis project atmospheric infrared sounder observations. </div>|
| [`fetch.amsu.reanalysis.yaml`](fetch.amsu.reanalysis.yaml) | <div align="left">UFS reanalysis project atmospheric Advanced Microwave Sounding Unit-A and B (AMSU-A and AMSU-B) observations. </div>|
| [`fetch.atms.reanalysis.yaml`](fetch.atms.reanalysis.yaml) | <div align="left">UFS reanalysis project atmospheric Advanced Technology Microwave Sounder (ATMS) observations. </div>|
| [`fetch.cris.reanalysis.yaml`](fetch.cris.reanalysis.yaml) | <div align="left">UFS reanalysis project atmospheric Cross-track Infrared Sounder (CrIS) observations. </div>|
| [`fetch.gpsro.reanalysis.yaml`](fetch.gpsro.reanalysis.yaml) | <div align="left">UFS reanalysis project atmospheric Global Positioning System Radio Occultation observations. </div>|
| [`fetch.hirs.reanalysis.yaml`](fetch.hirs.reanalysis.yaml) | <div align="left">UFS reanalysis project atmospheric High-resolution Infrared Radiation Sounder observations. </div>|
| [`fetch.sst.reanalysis.yaml`](fetch.sst.reanalysis.yaml) | <div align="left">UFS reanalysis project ocean sea-surface temperature observations. </div>|

</div>

#

Please direct questions to [Henry
R. Winterbottom](mailto:henry.winterbottom@noaa.gov?subject=[UFS-Applications])