import os
import sys


try:
    from library.common.action import Keyboard
    from library.windows.api import Windows_api

except (ImportError, ModuleNotFoundError):
    dir_path = (os.path.realpath(__file__)).rsplit("\\library", 1)[0]
    sys.path.append(dir_path)

    from library.common.action import Keyboard
    from library.windows.api import Windows_api
    

