CAR -- Count Archive Root entries
=================================


Introduction
------------

CAR is a Python 3 utility to count the number of entities at the root of an archive. For example, given the following archive file:

<pre>
	something.zip
	|- folder1
	   |- file11
	   |- file12
	|- file1
	|- file2
</pre>

If extracting `something.zip` to current folder, and if current folder already contains some files, since the extracted entities are `folder1`, `file1`, `file2`, or even more when the archive is big, it may mess up current directory. 

On the other hand, given the following archive file:

<pre>
	another.tar
	|- folder2
	   |- file21
	   |- file22
	   |- file23
	   |- file24
</pre>

If we extract its content to a new directory `another/`, then there will be an extra layer of directory, the extra depth introduced of which is not always desirable. 

Of course we can open the archive file in GUI or list its content in command line to help decide whether to extract it all to the current directory, or make a new directory for its content before extracting; but if the list of content file is huge, it soon becomes tedious to find out its pattern. This is the problem this utility attempts to solve.


Usage Example
-------------

Take above two ememplary virtual archives:

	car something.zip another.tar

The output will be:

	3 something.zip
	1 another.tar


Mechanism
---------

1. Determine archive type using Python `magic` module.
2. If it's a ZIP archive, use Python `zipfile` package to get its content; if TAR archive, use Python `tarfile` package to get its content; if GZIP-compressed TAR archive, use Python `tarfile` package to get its content.
3. Parse the content list and count the root entities.


Currently Supported Archive Type
--------------------------------

* ZIP archive
* TAR archive
* GZIP-compressed TAR archive


Currently Supported Platform
----------------------------

* Any platform with dependencies listed below.


Dependencies
------------

* [magic](https://pypi.python.org/pypi/python-magic/), used to get the archive type

These dependencies may have been included in your Python 3 distribution:

* pathlib
* zipfile
* tarfile


Known Issues
------------

* `magic` module may not work well on Windows 64 bit system. 
