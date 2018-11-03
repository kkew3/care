CARE -- Count Archive Root entries
==================================


Introduction
------------

`care` is a Python 3 utility to count the number of entities at the root of an archive. For example, given the following archive file:

	something.zip
	|- folder1
	   |- file11
	   |- file12
	|- file1
	|- file2

If extracting `something.zip` to current folder, and if current folder already contains some files, since the extracted entities are `folder1`, `file1`, `file2`, or even more when the archive is big, it may mess up current directory. 

On the other hand, given the following archive file:

	another.tar
	|- folder2
	   |- file21
	   |- file22
	   |- file23
	   |- file24

If we extract its content to a new directory `another/`, then there will be an extra layer of directory, the extra depth introduced of which is not always desirable. 

Of course we can open the archive file in GUI or list its content in command line to help decide whether to extract it all to the current directory, or make a new directory for its content before extracting; but if the list of content file is huge, it soon becomes tedious to find out its pattern. This is the problem this utility attempts to solve.


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

	usage: care [-h] [-T {zip,tar,7z} | -M | -W] [-f | -l] archive

	(C)ount (a)rchive (r)oot (e)ntries. Count entries at the root of an archive
	file so that one may decide whether or not to unpack it to a new folder or to
	the current folder without messing up other files under the current folder. If
	``magic`` module, installed via pip by name ``python-magic``, is not found,
	and the file type is not provided explicity via command line options, then
	filename extension will be used to guess the archive type. The return code: 0)
	success; 1) if the archive type is not recognizable; 2) if error is raised
	when opening the archive. Currently supported archive type: ZIP, TAR, GZ-
	compressed TAR, BZ2-compressed TAR, XZ-compressed TAR, and 7Z. For 7z support,
	``libarchive-dev`` should have been installed using, say, ``apt`` in
	Debian/Ubuntu; and ``libarchive`` package via ``pip``.

	positional arguments:
	  archive               the archive file

	optional arguments:
	  -h, --help            show this help message and exit
	  -T {zip,tar,7z}, --file-type {zip,tar,7z}
				the file type of ARCHIVE, where "tar" option includes
				TAR archive and that compressed by gzip, bzip2, or XZ
	  -M, --no-magic        don't even attempt to import `magic` module
	  -W, --no-ext-warning  suppress warning into stderr when `magic` module
				cannot be found
	  -f, --with-filename   print the count as: "${count} ${filename}"
	  -l, --list            rather than print the count, list all unique root
				entries


Mechanism
---------

1. Determine archive type using either: manual specification at command line, `magic` module, or filename extension.
2. If it's a ZIP archive, use Python `zipfile` package to get its content; if TAR archive, use Python `tarfile` package to get its content; if GZIP-compressed TAR archive, use Python `tarfile` package to get its content.
3. Parse the content list and count the root entities.


Currently Supported Archive Type
--------------------------------

* ZIP archive
* TAR archive
* GZIP/BZIP2/XZ-compressed TAR archive


Currently Supported Platform
----------------------------

* Any platform with dependencies listed below.


Dependencies
------------

### Optional

* [magic](https://pypi.python.org/pypi/python-magic/), used to get the archive type. Without `magic` module, the utility guesses archive type according to its filename, which can be of limited functionality under some circumstances. Can be installed by `pip3 install python-magic`.
* [libarchive](https://pypi.org/project/libarchive/), used to read 7z entries. Can be installed by `pip3 install libarchive`. Note that `libarchive-dev` is necessary to successfully install this package.
* [libarchive-dev](https://packages.debian.org/sid/libarchive-dev), dependency of `libarchive`.

How to install all the optional dependencies at once (Debian/Ubuntu):

```bash
sudo apt install libarchive-dev
pip3 install -r requirements.txt
```

### Should be part of Python 3 standard library

* pathlib
* zipfile
* tarfile
