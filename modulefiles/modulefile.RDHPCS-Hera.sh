#!/bin/bash --posix

################################################################################
## 
## Script name:         modulefiles/modulefile.RDHPCS-Hera.sh
##
## Script description:  Load the specified application(s) run-time
##                      environment(s) for the respective supported
##                      platform.
##
## Author:              Henry R. Winterbottom 
##
## Date:                2022-12-19         
##
## Script history log:  
##
##   2022-12-19: Henry R. Winterbottom -- Original version.
##
## Usage: sh modulefile.RDHPCS-Hera.sh
##
##   Imported Shell Variables:
##
##     HOMEufs:          The top-level working directory for all UFS
##                       applications.
##
##     If the following imported shell variables are equal to 1 in the
##     run-time environment, the respective application modules will
##     be loaded.
##
##     UFS_LAUNCH:       UFS workflow environment variable for the UFS
##                       launcher application.
##
##     UFS_STAGE:        UFS workflow environment variable for the UFS
##                       staging application.
##
##   Exported Shell Variables:
##
## Remarks:
##
##   Condition codes:
##
##      0 - no problem encountered
##     >0 - some problem encountered
##
## Attributes:
##
##   Language: POSIX shell
##   Machine:  Linux
##
################################################################################

set -e -u

#----

# Function
# --------

# exit_script.sh

# This function lists the loaded modules and exits gracefully.

exit_script(){

    # List the loaded modules.
    module list
}

#----

# Function
# --------

# load_modules.sh

# This function loads the modules for the respective UFS application
# task; once the module suite has been loaded, the modules are listed
# and the script exits gracefully.

load_modules(){

    # Query the run-time environment and proceed accordingly.
    if [[ ${UFS_LAUNCH} -eq 1 ]]; then

	# Load the modules for the respective application.
	. ${MODULESufs}/launch.env

	# List modules and exit gracefully.
	exit_script

    fi # [[ ${UFS_LAUNCH} -eq 1 ]]   

    # Query the run-time environment and proceed accordingly.
    if [[ ${UFS_STAGE} -eq 1 ]]; then

	# Load the modules for the respective application.
	. ${MODULESufs}/stage.env

	# List modules and exit gracefully.
	exit_script

    fi # [[ ${UFS_STAGE} -eq 1 ]]   
}

#----

# (1) Define the path to all UFS application environment variables for
#     the respective supported platform.
export MODULESufs=${HOMEufs}/modulefiles/platforms/rdhpcs-hera

# (2) Define the platform specific environment attributes.
. ${HOMEufs}/modulefiles/platforms/platform.rdhpcs-hera.env

# (3) Load the respective application module(s) for the supported
#     platform.
load_modules
