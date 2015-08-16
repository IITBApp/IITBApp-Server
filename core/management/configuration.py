__author__ = 'dheerendra'

import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def write_to_stdout(text):
    sys.stdout.write(bcolors.OKGREEN + str(text) + bcolors.ENDC)
    sys.stdout.flush()


def write_to_stderr(text):
    sys.stderr.write(bcolors.FAIL + str(text) + bcolors.ENDC)
    sys.stderr.flush()