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
	another.zip
	|- folder2
	   |- file21
	   |- file22
	   |- file23
	   |- file24
</pre>

If we extract its content to a new directory `another/`, then there will be an extra layer of directory, the extra depth introduced of which is not always desirable. 

Of course we can open the archive file in GUI or list its content in command line to help decide whether to extract it all to the current directory, or make a new directory for its content before extracting; but if the list of content file is huge, it soon becomes tedious to find out its pattern. This is the problem this utility attempts to solve.


Mechanism
---------

1. Determine archive type using `file $filename` utility.
2. If it's a ZIP archive, use `zip -l $filename` to get its content; if TAR archive, use `tar tf $filename` to get its content; if GZIP-compressed TAR archive, use `tar tzf $filename` to get its content.
3. Parse the content list and count the root entities.


Currently Supported Archive Type
--------------------------------

* ZIP archive
* TAR archive
* GZIP-compressed TAR archive


Currently Supported Platform
----------------------------

* Linux, with `file`, `zip`, `tar` utilities on `PATH`.


Dependencies
------------

* [chardet](https://pypi.python.org/pypi/chardet), used to correctly parse the output 
