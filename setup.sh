#!/bin/sh 

setenv HOMEufs /Users/henry.winterbottom/trunk/UFS/ufs_apps
setenv PREufs ${HOMEufs}/modulefiles/modulefile.osx.sh
setenv YAMLufs ${HOMEufs}/parm/ufs.reanalysis.yaml
setenv CYCLEufs 20200101060000
setenv WORKufs /Users/henry.winterbottom/work
setenv EXPTufs UFS_LAUNCH_APP

setenv PYTHONPATH /Users/henry.winterbottom/trunk/UFS/ufs_pyutils:${HOMEufs}/ush
