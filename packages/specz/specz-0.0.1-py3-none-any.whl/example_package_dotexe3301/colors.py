# responsible for text colors in terminal
import sys


def red(string):
    sys.stdout.write("\033[91m" + string + "\033[0m")


def green(string):
    sys.stdout.write("\033[92m" + string + "\033[0m")


def yellow(string):
    sys.stdout.write("\033[93m" + string + "\033[0m")


def blue(string):
    sys.stdout.write("\033[34m" + string + "\033[0m")


def magenta(string):
    sys.stdout.write("\033[95m" + string + "\033[0m")


def cyan(string):
    sys.stdout.write("\033[36m" + string + "\033[0m")


def underline(string):
    sys.stdout.write("\033[4m" + string + "\033[0m")
