# operates the functionality of taking input from the user
import os
from colors import *


def starter():
    path = os.getcwd()
    inp = input(path + ">").strip()
    if os.path.exists(inp):
        if os.path.isfile(inp):
            return [1, inp]
        elif os.path.isdir(inp):
            return [0, inp]
    else:
        red('InvalidPathError: Either path does not exist or given is not an string. Please give absolute path with '
            'extension of file.')
