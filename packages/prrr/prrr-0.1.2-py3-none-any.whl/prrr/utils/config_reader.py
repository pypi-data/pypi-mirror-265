# This def function reads .prr file and returns ots content
import os


def read():
    # read file from current directory
    return open(os.curdir + '/.prr', 'r').read()
