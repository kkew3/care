#!/usr/bin/python3

__author__ = 'Kaiwen Wu'
__version__ = '1.1-alpha'


import argparse
import sys
import glob
import zipfile
import tarfile
import magic
from pathlib import PurePath


def make_parser():
    parser = argparse.ArgumentParser(description='Count Archive Root entries. '
            'Count entries at root of a '
            'archive file so that one can decide whether or not to unpack it to a '
            'new folder or to the current folder without messing up other '
            'files under the current folder. Require `unzip`, `tar` command '
            'on PATH.', epilog='Currently support .zip, .tar, .tar.gz types.')
    parser.add_argument('afile', nargs='+', help='the archive file(s) whose '
            'root entries are to be counted')
    return parser


class UnrecognizableArchiveError(BaseException): pass

def get_archive_entries(filename):
    mime = magic.from_file(filename)
    if 'Zip archive' in mime:
        try:  # just in case
            with zipfile.ZipFile(filename) as infile:
                entries = map(PurePath, infile.namelist())
        except zipfile.BadZipFile:
            raise UnrecognizableArchiveError()
    elif 'tar archive' in mime or 'gzip compressed data' in mime:
        try:
            with tarfile.open(filename) as infile:
                entries = map(PurePath, infile.getnames())
        except tarfile.ReadError:
            raise UnrecognizableArchiveError()
    else:
        raise UnrecognizableArchiveError()
    return entries  # iter object, not list

def count_root_entries(entry_names):
    """
    :param entry_names: the names of entries in the archive
    :return: the count of root entries
    """
    def get_root_entry(splitted_entry):
        root = None
        if len(splitted_entry):
            if splitted_entry[0] in ('.', '..'):
                if len(splitted_entry) > 1:
                    root = splitted_entry[1]
            else:
                root = splitted_entry[0]
        return root
    splitted_entries = map(lambda e: e.parts, entry_names)
    root_entries = map(get_root_entry, splitted_entries)
    nonempty_root_entries = set(filter(lambda r: r is not None, root_entries))
    rec = len(nonempty_root_entries)  # the count
    return rec



def main():
    args = make_parser().parse_args(sys.argv[1:])
    afiles = []
    for globfilename in args.afile:
        for filename in glob.iglob(globfilename):
            afiles.append(filename)
    for filename in afiles:
        try:
            entries = get_archive_entries(filename)
            rec = count_root_entries(entries)
            print(rec, filename)
        except UnrecognizableArchiveError:
            print('skipped unrecognized archive:', filename, file=sys.stderr)

if __name__ == '__main__':
    main()
