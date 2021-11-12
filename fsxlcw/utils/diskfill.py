#!/usr/bin/env python3
"""
Create some binary files to fill up the filesystem
"""

import argparse
import os

def generate_big_random_bin_file(directory, file_name, size):
    """
    generate big binary file with the specified size in bytes
    :param directory: the parnt directory where the files will be created
    :param file_name: the file name
    :param size: the size in bytes
    :return:void
    """

    # create the folder that will contain the files
    if not os.path.isdir(directory):
        raise SystemExit(f"OBS! The directory {directory} doesn't exist")

    directory = directory.rstrip("/")
    with open( f"{directory}/RANDOM_{file_name}", 'wb' ) as fout:
        fout.write(os.urandom(size))
        print( f"created file: {directory}/RANDOM_{file_name}" )

    pass


def generate_file_name():
    """
    Generate a random string
    """
    import string
    import random # define the random module

    S = 10  # number of characters in the string.
    # call random.choices() string module to find the string in Uppercase + numeric data.
    ran = ''.join( random.choices( string.ascii_uppercase + string.digits, k = S ))

    # print("The randomly generated string is : " + str(ran)) # print the random data
    return ran


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("parent_directory",
        help="the directory where to create files")
    parser.add_argument("-n", "--number_of_files",
        help="how many files of 100MB will be created")
    args = parser.parse_args()

    # size: 100MB file  = 100.000.000 bytes
    size = 100000000
    the_range = 100
    if args.number_of_files:
        the_range = int(args.number_of_files)
    parent_directory = args.parent_directory

    for x in range(the_range):
        file_name = generate_file_name()
        generate_big_random_bin_file(parent_directory, file_name, size)

    print( f"generated {the_range} file(s) of size {size/1000} MB in {parent_directory}" )


if __name__ == "__main__":
    main()