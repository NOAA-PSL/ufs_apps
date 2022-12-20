# Unified Forecast System Workflow Staging

The Unified Forecast System (UFS) workflow staging applies to the
fetching (i.e., collecting) and storing (i.e., saving) of specified
files. This README provides a description of the available
YAML-formatted configuration options.

## Building a Fetching Application Configuration

The following YAML snippet provides an example architecture for the
YAML-formatted configuration files to be used for the UFS fetching
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
| `checksum` | <div align="left">This optional attribute provides information relevant to the determination of checksum hash values for each file collected for the respective interface/platform; a list of currently supported values can be found [here](#checksum-configuration-attributes).</div> |
| `[interface_platform]` | <div align="left">This value defines the platform and/or interface from which to fetch files; the currently (only) supported option is `aws_s3` which should replace the `[interface_platform]` reference key.</div> |
| `[fetching_option]` | <div align="left">This value defines the types/contents of the file identifiers to follow; as an example, for ocean or atmosphere type observation files, this attribute may read `ocean_obs` or `atmos_obs`, respectively; the respective attributes may be used as optional command line arguments for the [fetching application script](https://github.com/HenryWinterbottom-NOAA/ufs_apps/blob/develop/scripts/exufs_fetch.py). </div> |
| `[file_identifier]` | <div align="left">This value assigns a unique name to the YAML key for the attributes corresponding to a given file to be retrieved; for example, [National Environmental Satellite, Data, and Information Service (NESDIS)](https://www.nesdis.noaa.gov/) hosted observations for sea-surface temperature (SST) derived from the [AVHRR](https://www.eumetsat.int/avhrr) instrument onboard the National Oceanic and Atmospheric (NOAA) 15 satellite may have a file identifier such as `sst.nesdis_avhrr_noaa15`. </div> | 

</div>

### Checksum Configuration Attributes

<div align="center">

| Attribute | Description |
| :-------------: | :-------------: |
| `aws_s3_filepath` | <div align="left">The local host path for the file to contain the checksum hash values for the AWS s3 interface/platform downloaded files.</div> |
| `aws_s3_hash` | <div align="left">The checksum hash types for the respective AWS s3 interface/platform downloaded files; currently supported values are `md5`, `sha1`, `sha224`, `sha256`, `sha384`, and `sha512`; if not specified, `md5` is assumed. |

</div>

An example YAML-formatted configuration file using each of the
attributes defined above might be as follows.

~~~
# All attributes that follow are for the UFS fetching application.
fetch:

     # Define the checksum hash index attributes.
     checksum:

       aws_s3_filepath: !ENV ${WORKufs}/${EXPTufs}/com/${CYCLEufs}/aws_s3.fetch.obs.md5     
       aws_s3_hash: md5
  
     # Define a supported the platform/interface from which to collect
     # the respective files.
     aws_s3:	 

          # Define the fetching type; this corresponds to ocean
          # observations.
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
| `local_path` | <div align="left">The file path on the local host to where the fetched file will be staged; environment variables and POSIX compliant time and date string attributes are supported when building this attribute. | This value is required for all platforms/interfaces | </div>
| `object_path` | <div align="left">The AWS s3 object path beneath the AWS s3 `bucket` attribute defined above; environment variables and POSIX compliant time and date string attributes are supported when building this attribute.| `aws_s3` | </div> 
| `profile_name` | <div align="left">The AWS s3 profile to be used for AWS s3 platform/interface file fetching; this value should be a profile name within the respective user `~/.aws/credentials` file path; if fetching from a public bucket this value should be set to `null`. | `aws_s3` |</div>

</div>

<div align="center">

| Optional Attribute | Description | | Default Value | 
| :-------------: | :-------------: | :-------------: |
| `ignore_missing` | <div align="left">This is boolean value specifying whether to fail for missing platform/interface file paths (`False`) or to ignore a missing file and continue to process the attributes within the YAML-formatted configuration file (`True`). | `False` | </div>
| `multifile` |  <div align="left">See section [multifile configuration attributes](#multifile_configuration_attributes) below. | option is ignored | </div> 
| `nc_concat` | <div align="left">See section [netCDF concatenation configuration attribues](#netcdf_multifile_concatenation_attributes) (below). | option is ignored | </div> |
| `offset_seconds` | <div align="left">The total number of offset seconds relative to the forecast date for valid files; this value is used to define any POSIX compliant time and date string information specified in `local_path`; this value is also used to build the `object_path` (see above). | 0 | </div>

</div>



### Multifile Configuration Attributes




### netCDF Multifile Concatenation Attributes