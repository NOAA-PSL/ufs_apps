# Unified Forecast System Workflow Staging Configurations

The Unified Forecast System (UFS) workflow staging applies to the
fetching (i.e., collecting) and storing (i.e., saving) of specified
files. This README provides a description of the available
YAML-formatted configuration options.

### Fetching Application Configuration

The following YAML snippets provide an example for the architecture of
the YAML-formatted configuration file for fetching user-specified
files. Explanations of the respective attributes are provided in the
table which follows.

~~~
fetch:
     checksum:
          .
	  .
          .
	  
     [interface_platform]:
     
          [fetching_option]:
	  
	       [file_identifier]:
                    .
		    .
		    .
~~~

<div align="center">

| Attribute | Description |
| :-------------: | :-------------: |
| `fetch` | <div align="left">This attribute is mandatory for all fetching applications; this informs the application as to the relevant configuration attributes.</div> | 
| `checksum` | <div align="left">This optional attribute provides information relevant to the determination of checksum hash values for each file collected for the respective interface/platform; a list of currently supported values can be found [here](#checksum-attributes).</div> |
| `[interface_platform]` | <div align="left">This value defines the platform and/or interface from which to fetch files; the currently (only) supported option is `aws_s3` which should replace the `[interface_platform]` reference key.</div> |
| `[fetching_option]` | <div align="left">This value defines a type of file; </div> | 

</div>

#### `checksum` Attributes

<div align="center">

| Attribute | Description |
| :-------------: | :-------------: |
| `aws_s3_filepath` | <div align="left">The local host path for the file to contain the checksum hash values for the AWS s3 interface/platform downloaded files.</div> |
| `aws_s3_hash` | <div align="left">The checksum hash types for the respective AWS s3 interface/platform downloaded files; currently supported values are `md5`, `sha1`, `sha224`, `sha256`, `sha384`, and `sha512`; if not specified, `md5` is assumed. |

</div>