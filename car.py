#!/usr/bin/python3

__author__ = 'Kaiwen Wu'
__version__ = '1.1-alpha'


import argparse
import sys
import glob
import zipfile
import tarfile
from pathlib import PurePath

def attempt_import_magic(importwarning):
    """
    :param importwarning: True to print the warning message
    """
    try:
        import magic
        assert 'magic' in dir()
    except (OSError, ImportError):
        if importwarning:
            print('Warning: error loading `magic` library; '
                  'use filename to guess archive type', file=sys.stderr)

def make_parser():
    parser = argparse.ArgumentParser(description='Count Archive Root entries. '
            'Count entries at root of a '
            'archive file so that one can decide whether or not to unpack it to a '
            'new folder or to the current folder without messing up other '
            'files under the current folder. If `magic` module '
            '(`pip install python-magic`) is not found, filename extension '
            'will be used to guess the archive type. The return code is 0 '
            'if there is no unrecognized archive; otherwise it\'s 1.', 
            epilog='Currently support .zip, .tar, .tar.gz types.')
    parser.add_argument('afile', nargs='+', help='the archive file(s) whose '
            'root entries are to be counted')
    parser.add_argument('-M', dest='importmagic', help='don\'t even attempt '
            'to import `magic` module', action='store_false')
    parser.add_argument('-W', dest='importwarning', help='suppress warning '
            'into stderr when `magic` module cannot be found', 
            action='store_false')
    parser.add_argument('-S', dest='showskip', help='don\'t print '
            'unrecognized archives to stderr before skipping them', 
            action='store_false')
    return parser


class UnrecognizableArchiveError(BaseException): pass

def guess_archive_type(filename):
    if 'magic' in dir():
        mime = magic.from_file(filename)
        if 'Zip archive' in mime:
            archive_type = 'zip'
        elif 'tar archive' in mime or 'gzip compressed data' in mime:
            archive_type = 'tar'  # tar or compressed tar
        else:
            raise UnrecognizableArchiveError()
    else:
        if filename.endswith('.zip'):
            archive_type = 'zip'
        elif any([filename.endswith('.tar'),
                  filename.endswith('.tar.gz'),
                  filename.endswith('.tgz')]):
            archive_type = 'tar'  # tar or compressed tar
        else:
            raise UnrecognizableArchiveError()
    return archive_type

def get_archive_entries(filename, archive_type):
    if archive_type == 'zip':
        try:  # just in case
            with zipfile.ZipFile(filename) as infile:
                entries = map(PurePath, infile.namelist())
        except zipfile.BadZipFile:
            raise UnrecognizableArchiveError()
    elif archive_type == 'tar':
        try:
            with tarfile.open(filename) as infile:
                entries = map(PurePath, infile.getnames())
        except tarfile.ReadError:
            raise UnrecognizableArchiveError()
    else:
        # shouldn't reach here though
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
    if args.importmagic:
        attempt_import_magic(args.importwarning)
    afiles = []
    retcode = 0
    for globfilename in args.afile:
        for filename in glob.iglob(globfilename):
            afiles.append(filename)
    for filename in afiles:
        try:
            archive_type = guess_archive_type(filename)
            entries = get_archive_entries(filename, archive_type)
            rec = count_root_entries(entries)
            print(rec, filename)
        except UnrecognizableArchiveError:
            retcode = 1
            if args.showskip:
                print('skipped unrecognized archive:', filename, 
                      file=sys.stderr)
    return retcode

if __name__ == '__main__':
    retcode = main()
    sys.exit(retcode)
