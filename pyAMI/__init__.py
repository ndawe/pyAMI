# Only allow pyAMI to import if using the same sys.version as was used to build
# pyAMI and its dependencies

import sys

BUILD_SYS_VERSION = (2, 7)
if sys.version_info[:2] != BUILD_SYS_VERSION:
    raise ImportError(
            'This pyAMI installation was built against Python %d.%d '
            'but you are using Python %d.%d' % (
                BUILD_SYS_VERSION +
                sys.version_info[:2]))

