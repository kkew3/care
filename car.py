#!/usr/bin/python3

__author__ = 'Kaiwen Wu'
__version__ = '1.0-beta'


import argparse
from subprocess import Popen, PIPE
from sys import argv
import glob
import chardet
import os
import re


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

def parse_unpack_list(unpackcmd):
    """
    :param unpackcmd: a list to feed subprocess.Popen
    :return: a list of stdout
    """
    with Popen(unpackcmd, stdout=PIPE) as proc:
        bcontent = proc.stdout.read()
    ec = chardet.detect(bcontent)['encoding']
    content = bcontent.decode(encoding=ec)
    unpacklist = content.split('\n')
    return unpacklist

def parse_zip_list(zipfile):
    """
    :param zipfile: path to an existing zip file
    :return a list of *useful* lines to parse
    """
    unziplist = parse_unpack_list(['unzip', '-l', zipfile])
    start_line = None
    for lid, line in enumerate(unziplist):
        if line.strip().split() == ['Length', 'Date', 'Time', 'Name']:
            start_line = lid + 2
    unziplist = unziplist[start_line:-3]
    unziplist = [x.split(maxsplit=3)[-1] for x in unziplist]
    return unziplist

def parse_tar_list(tarfile):
    untarlist = parse_unpack_list(['tar', 'tf', tarfile])
    untarlist = [x[2:] if x.startswith('./') else x for x in untarlist]
    untarlist = [x for x in untarlist if x.strip() != '']
    return untarlist

def parse_tgz_list(tgzfile):
    untgzlist = parse_unpack_list(['tar', 'tzf', tgzfile])
    untgzlist = [x[2:] if x.startswith('./') else x for x in untgzlist]
    untgzlist = [x for x in untgzlist if x.strip() != '']
    return untgzlist

def parse_entries(entry_names):
    """
    :param entry_names: the names of entries in the archive
    :return: the count of root entries
    """
    splitted_entries = [os.path.split(x) for x in entry_names]
    rootdirs = set(x[0] for x in splitted_entries if len(x[0]))
    rootdirs = set(re.split(r'[/\\]', x)[0] for x in rootdirs)  # get the root directory
    rootfiles = set(x[1] for x in splitted_entries if not len(x[0]) and len(x[1]))
    rec = len(rootdirs) + len(rootfiles)  # the root entries count
    return rec

def get_filelist_parser(filename):
    with Popen(['file', filename], stdout=PIPE) as proc:
        content = proc.stdout.read().decode(encoding='ascii')
    parser = None
    if 'gzip compressed data' in content:
        parser = parse_tgz_list
    elif 'tar archive' in content:
        parser = parse_tar_list
    elif 'Zip archive' in content:
        parser = parse_zip_list
    return parser
    

def main():
    args = make_parser().parse_args(argv[1:])
    afiles = []
    for globfilename in args.afile:
        for filename in glob.iglob(globfilename):
            afiles.append(filename)
    for filename in afiles:
        stdout_parser = get_filelist_parser(filename)
        if stdout_parser is None:
            print('! unrecognized archive; skipped:', filename)
        else:
            unpacklist = stdout_parser(filename)
            rec = parse_entries(unpacklist)
            print(rec, filename)

if __name__ == '__main__':
    main()
