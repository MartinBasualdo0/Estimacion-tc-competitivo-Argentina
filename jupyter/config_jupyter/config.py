import sys
import os

def set_wd():
    sys.path.append(os.path.abspath('../'))
    dir = os.getcwd()
    os.chdir(dir.replace("\\jupyter", ""))
    return os.getcwd()
