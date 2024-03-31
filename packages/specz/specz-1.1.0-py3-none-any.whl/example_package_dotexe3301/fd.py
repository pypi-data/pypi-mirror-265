from colors import *
from utils import utility
import os
import stat
import datetime


def formatter(prop: str, value: str):
    # takes two strings and make prop string left align and return combination of two given strings
    blue("  |-- ")
    print(prop.ljust(20, " ") + value)


def extract_permissions(st_mode):
    permissions = {
        'owner': {
            'read': bool(st_mode & stat.S_IRUSR),
            'write': bool(st_mode & stat.S_IWUSR),
            'execute': bool(st_mode & stat.S_IXUSR)
        },
        'group': {
            'read': bool(st_mode & stat.S_IRGRP),
            'write': bool(st_mode & stat.S_IWGRP),
            'execute': bool(st_mode & stat.S_IXGRP)
        },
        'others': {
            'read': bool(st_mode & stat.S_IROTH),
            'write': bool(st_mode & stat.S_IWOTH),
            'execute': bool(st_mode & stat.S_IXOTH)
        }
    }
    return permissions


def spec(path: str):
    blue("File\n")
    blue("  |\n")
    blue("  |-- ")

    print("File".ljust(20, " "), end="")
    yellow(os.path.basename(path).split('/')[-1] + "\n")

    formatter("Size",
              str(os.path.getsize(path)) + " Bytes (" + str(round(os.path.getsize(path) / 1024 / 1024, 4)) + ") MB")

    formatter("Location", os.path.abspath(path))

    blue("  |-- ")
    print("Creation Time".ljust(20, " "), end="")
    green(datetime.datetime.fromtimestamp(os.path.getctime(path)).strftime('%d-%b-%Y  %H:%M:%S') + "\n")

    blue("  |-- ")
    print("Last Modified".ljust(20, " "), end="")
    red(datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d-%b-%Y  %H:%M:%S') + "\n")

    extension = os.path.splitext(path)[1].lower()
    ft = utility.file_type[extension] if extension in utility.file_type else "Can't identify file type"
    formatter("Type of File", ft + " (" + extension + ")")

    permissions = extract_permissions(os.stat(path).st_mode)
    blue("  |-- ")
    magenta("Permissions")
    blue("--------")
    print("owner: ", end=" ")
    green("read\t") if permissions['owner']['read'] else red("read\t")
    green("write\t") if permissions['owner']['write'] else red("write\t")
    green("execute\n") if permissions['owner']['execute'] else red("execute\n")
    blue("      \t\t\t|--------")
    print("group: ", end=" ")
    green("read\t") if permissions['group']['read'] else red("read\t")
    green("write\t") if permissions['group']['write'] else red("write\t")
    green("execute\n") if permissions['group']['execute'] else red("execute\n")
    blue("      \t\t\t|-------")
    print("others: ", end=" ")
    green("read\t") if permissions['others']['read'] else red("read\t")
    green("write\t") if permissions['others']['write'] else red("write\t")
    green("execute\n") if permissions['others']['execute'] else red("execute\n")
