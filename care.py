
# To support archive with non-ASCII path name entries, make changes to
# ${VIRTUAL_ENV}/lib/python3.6/site-packages/libarchive/adapters/archive_read.py
# as per https://github.com/dsoprea/PyEasyArchive/issues/52.

__author__ = 'Kaiwen Wu'
__version__ = '2.3'
__description__ = '''(C)ount (a)rchive (r)oot (e)ntries.
Count entries at the root of an archive file so that one may decide whether or
not to unpack it to a new folder or to the current folder without messing up
other files under the current folder. The return code: 0) success;
1) if error is raised when opening the archive. Support all archive types
``libarchive`` supports.'''.replace('\n', ' ')

import sys
import argparse
import logging

import libarchive.public
import libarchive.exception


def make_parser():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('filename', metavar='FILE', help='the archive file')
    parser.add_argument('-l', '--list', dest='list_entries',
                        action='store_true',
                        help=('rather than print the count, list all unique '
                              'root entries'))
    return parser


# ValueError hazard
# - read filename failure
# - illegal pathname
def get_root_entries(filename):
    root_entries = []
    with libarchive.public.file_reader(filename) as infile:
        for entry in infile:
            root_entry = entry.pathname.split('/', maxsplit=1)[0]
            if not root_entry:
                raise ValueError('absolute path as archive entry: "{}"'
                                 .format(entry.pathname))
            if root_entry in ['.', '..']:
                raise ValueError(
                    'unsupported path as archive entry: beginning with '
                    '. or ..')
            root_entries.append(root_entry)
    root_entries = list(set(root_entries))  # order is not required
    return root_entries


def print_report(root_entries, list_entries: bool):
    """
    Print the number of root entries, and a list of all root entries (if
    ``list_entries`` is ``True``).
    """
    if list_entries:
        for line in root_entries:
            print(line)
    else:
        print(len(root_entries))


def main():
    logging.basicConfig(level=logging.WARNING,
                        format='%(levelname)s: %(message)s')
    args = make_parser().parse_args()
    try:
        root_entries = get_root_entries(args.filename)
    except (libarchive.exception.ArchiveError, ValueError):
        logging.exception('failed to read "%s"', args.filename)
        return 1
    print_report(root_entries, args.list_entries)
    logging.shutdown()
    return 0


if __name__ == '__main__':
    sys.exit(main())
