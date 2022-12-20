# Unified Forecast System Workflow Staging Configurations

The Unified Forecast System (UFS) workflow staging applies to the
fetching (i.e., collecting) and storing (i.e., saving) of specified
files. This README provides a description of the available
YAML-formatted configuration options.

## Fetching Application Configuration

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
	  
     <interface_platform>:
     
          <fetching_option>:
	  
	       <file_identifier>:
                    .
		    .
		    .
~~~

<div align="center">

| YAML Attribute | Description |
| :-------------: | :-------------: |
| `fetch` | <div align="left">This attribute is mandatory for all fetching applications; this informs the application as to the relevant configuration attributes.</div> | 
| `checksum` | <div align="left">This optional attribute provides information relevant to the determination of checksum hash values for each file collected for the respective interface/platform; a list of currently supported values can be found [here](https://www.google.com).</div> | 

</div>