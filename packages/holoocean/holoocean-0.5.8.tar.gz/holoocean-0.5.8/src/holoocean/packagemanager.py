"""Package manager for worlds available to download and use for HoloOcean"""

import sys

def install(package_name, url=None, branch=None, commit=None):
    """Throws an error to remind the user that HoloOcean is no longer supported via pypi.
    """
    sys.exit("\033[91mFatal Error: Due to Unreal Engine EULA changes and requirements, HoloOcean can no longer be installed via pypi (An empty installation was installed instead and should be removed). However, HoloOcean can still be easily installed. Please visit the updated installation instructions at https:\\\\holoocean.readthedocs.io for more details.")
