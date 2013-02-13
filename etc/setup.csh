# This script is to be sourced by [t]csh.

if ( ($?PYAMI_HOME) ) then
    set DIR_PYAMI_SETUP=$PYAMI_HOME
    set SOURCE_PYAMI_SETUP=$DIR_PYAMI_SETUP"/setup.csh"
else
    # determine path to this script
    # http://stackoverflow.com/questions/4617758/problem-getting-full-path-of-a-shell-script-while-using-tcsh
    set SOURCE_PYAMI_SETUP=($_)
    if ("$SOURCE_PYAMI_SETUP" != "") then
        set SOURCE_PYAMI_SETUP=$PWD/$SOURCE_PYAMI_SETUP[2]
    else
        echo "this script must be sourced"
        exit 1
    endif
    set DIR_PYAMI_SETUP=`(dirname "$SOURCE_PYAMI_SETUP")`
endif
echo "sourcing $SOURCE_PYAMI_SETUP"

setenv PATH $DIR_PYAMI_SETUP"/bin:$PATH"
if ( ! ($?PYTHONPATH) ) then
    setenv PYTHONPATH $DIR_PYAMI_SETUP/lib
else
    setenv PYTHONPATH $DIR_PYAMI_SETUP/lib":$PYTHONPATH"
endif
setenv PYAMI_VERSION `(cat "$DIR_PYAMI_SETUP"/version.txt)`
echo "setting up pyAMI $PYAMI_VERSION"
