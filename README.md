CARE -- Count Archive Root entries
==================================


Introduction
------------

`care` is a Python 3 utility to count the number of entities at the root of an archive. For example, given the following
archive file:

	something.zip
	|- folder1
	   |- file11
	   |- file12
	|- file1
	|- file2

If extracting `something.zip` to current folder, and if current folder already contains some files, since the extracted
entities are `folder1`, `file1`, `file2`, or even more when the archive is big, it may mess up current directory.

On the other hand, given the following archive file:

	another.tar
	|- folder2
	   |- file21
	   |- file22
	   |- file23
	   |- file24

If we extract its content to a new directory `another/`, then there will be an extra layer of directory, the extra depth
introduced of which is not always desirable.

Of course, we can open the archive file in GUI or list its content in command line to help decide whether to extract it
all to the current directory, or make a new directory for its content before extracting; but if the list of content file
is huge, it soon becomes tedious to find out its pattern. This is the problem this utility attempts to solve.


Installation
------------

```sh
# or use another name other than 'rt' ...
python3 -m virtualenv rt
. rt/bin/activate
pip install -r requirements.txt
bash make_bin.sh
deactivate
path_to_care="$(realpath bin/care)"
# assuming ~/bin in PATH, or go to another directory in PATH ...
cd ~/bin
ln -s "$path_to_care" care
```


Usage Example
-------------

Take above two ememplary virtual archives:

```bash
$ care something.zip
3
$ care -l something.zip
folder1
file2
file3
$ care another.tar
1
```

where `$` is the command line prompt.


Detailed usage
--------------

> Copied from `care --help`

    usage: care.py [-h] [-l] FILE
    
    (C)ount (a)rchive (r)oot (e)ntries. Count entries at the root of an archive
    file so that one may decide whether or not to unpack it to a new folder or to
    the current folder without messing up other files under the current folder.
    The return code: 0) success; 1) if error is raised when opening the archive.
    Support all archive types ``libarchive`` supports.
    
    positional arguments:
      FILE        the archive file
    
    optional arguments:
      -h, --help  show this help message and exit
      -l, --list  rather than print the count, list all unique root entries

Currently Supported Platform
----------------------------

* Any platform with dependencies listed below.

Dependencies
------------

* [libarchive](https://pypi.org/project/libarchive/), used to open archive file.
