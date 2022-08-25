### slipit

----

*slipit* is a command line utility for creating archives with path traversal elements.
It is basically a successor of the famous [evilarc](https://github.com/ptoomey3/evilarc)
utility with an extended feature set and improved base functionality.

![](https://github.com/usdAG/slipit/workflows/main%20Python%20CI/badge.svg?branch=main)
![](https://github.com/usdAG/slipit/workflows/develop%20Python%20CI/badge.svg?branch=develop)
[![](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/usdAG/slipit/releases)
[![](https://img.shields.io/badge/build%20system-pip-blue)](https://pypi.org/project/slipit)
![](https://img.shields.io/badge/python-9%2b-blue)
[![](https://img.shields.io/badge/license-GPL%20v3.0-blue)](https://github.com/usdAG/slipit/blob/main/LICENSE)

```console
[user@host ~]$ slipit archive.tar.gz
?rw-r--r-- user/user         24 2022-08-25 10:57:35 legit.txt
[user@host ~]$ slipit archive.tar.gz file1.txt file2.txt
[user@host ~]$ slipit archive.tar.gz
?rw-r--r-- user/user         24 2022-08-25 10:57:35 legit.txt
?rw-r--r-- user/user          3 2022-08-25 10:56:41 ..\..\..\..\..\..\file1.txt
?rw-r--r-- user/user          3 2022-08-25 10:56:44 ..\..\..\..\..\..\file2.txt
[user@host ~]$ slipit archive.tar.gz file1.txt --depth 3 --increment 1
[user@host ~]$ slipit archive.tar.gz
?rw-r--r-- user/user         24 2022-08-25 10:57:35 legit.txt
?rw-r--r-- user/user          3 2022-08-25 10:56:41 ..\..\..\..\..\..\file1.txt
?rw-r--r-- user/user          3 2022-08-25 10:56:44 ..\..\..\..\..\..\file2.txt
?rw-r--r-- user/user          3 2022-08-25 10:56:41 ..\file1.txt
?rw-r--r-- user/user          3 2022-08-25 10:56:41 ..\..\file1.txt
?rw-r--r-- user/user          3 2022-08-25 10:56:41 ..\..\..\file1.txt
[user@host ~]$ slipit archive.tar.gz --clear
[user@host ~]$ slipit archive.tar.gz
?rw-r--r-- user/user         24 2022-08-25 10:57:35 legit.txt
```

### Installation

----

*slipit* can be installed via [pip](https://pypi.org/project/pip/) by running the following commands:

```console
$ git clone https://github.com/usdAG/slipit
$ cd slipit
$ python3 setup.py sdist
$ pip3 install --user dist/* 
```

*slipit* also supports autocompletion for *bash*. To take advantage of autocompletion, you need to have the
[completion-helpers](https://github.com/qtc-de/completion-helpers) project installed. If setup correctly, just
copying the [completion script](./resources/bash_completion.d/slipit) to your ``~/.bash_completion.d`` folder enables
autocompletion.


### Usage

----

```console
[user@host ~]$ slipit -h
usage: slipit [-h] [--archive-type {zip,tar,tgz,bz2}] [--clear] [--debug] [--depth int] [--increment int]
              [--overwrite] [--prefix string] [--multi] [--remove name] [--separator char] [--sequence seq]
              [--static content] [--symlink target] archive [filename ...]

slipit v1.0.0 - Utility for creating ZipSlip archives.

positional arguments:
  archive               target archive file
  filename              filenames to include into the archive

options:
  -h, --help            show this help message and exit
  --archive-type {zip,tar,tgz,bz2}
                        archive type to use
  --clear               clear the specified archive from traversal items
  --debug               enable verbose error output
  --depth int           number of traversal sequences to use (default=6)
  --increment int       add incremental traversal payloads from <int> to depth
  --overwrite           overwrite the target archive instead of appending to it
  --prefix string       prefix to use before the file name
  --multi               create an archive containing multiple payloads
  --remove name         remove files from the archive (glob matching)
  --separator char      path separator (default=\)
  --sequence seq        use a custom traversal sequence (default=..{sep})
  --static content      use static content for each input file
  --symlink target      add as symlink (only available for tar archives)
```

*slipit* expects the targeted output archive and an arbitrary number of input files as mandatory command line
parameters. All specified input files are appended to the specified archive including a path traversal prefix
with a depth specified with the `--depth` option (default is 6). The targeted archive format is determined
automatically depending on the file extension for non existing archives or by the mime type for already existing
archives. You can also specify the archive type manually by using the `--archive-type` option.

```console
[user@host ~]$ slipit example.zip 
File Name                                             Modified             Size
example/                                       2022-02-02 18:39:00            0
example/images/                                2022-02-02 18:40:16            0
example/images/holiday.png                     2022-02-02 18:40:06        34001
example/images/beach.png                       2022-02-02 18:40:16         2112
example/documents/                             2022-02-02 18:39:48            0
example/documents/invoice.docx                 2022-02-02 18:39:40         3001
example/documents/important.docx               2022-02-02 18:39:48          121
[user@host ~]$ slipit example.zip test.txt
[user@host ~]$ slipit example.zip 
File Name                                             Modified             Size
example/                                       2022-02-02 18:39:00            0
example/images/                                2022-02-02 18:40:16            0
example/images/holiday.png                     2022-02-02 18:40:06        34001
example/images/beach.png                       2022-02-02 18:40:16         2112
example/documents/                             2022-02-02 18:39:48            0
example/documents/invoice.docx                 2022-02-02 18:39:40         3001
example/documents/important.docx               2022-02-02 18:39:48          121
..\..\..\..\..\..\test.txt                     2022-02-02 18:40:48           36
```

*slipit* expects the specified input files to exist on your local file system and uses the file content of
them within the archive. Often times this is not necessary and you just require dummy content to test for
*ZipSlip* vulnerabilities. This is where the `--static <string>` option can be helpful. When using this option,
only the filenames of the specified input files are used within the archive, while their content is set to `<string>`.

```console
[user@host ~]$ slipit example.zip test2.txt --static 'HELLO WORLD :D'
[user@host ~]$ slipit example.zip 
File Name                                             Modified             Size
example/                                       2022-02-02 18:39:00            0
example/images/                                2022-02-02 18:40:16            0
example/images/holiday.png                     2022-02-02 18:40:06        34001
example/images/beach.png                       2022-02-02 18:40:16         2112
example/documents/                             2022-02-02 18:39:48            0
example/documents/invoice.docx                 2022-02-02 18:39:40         3001
example/documents/important.docx               2022-02-02 18:39:48          121
..\..\..\..\..\..\test.txt                     2022-02-02 18:40:48           36
..\..\..\..\..\..\test2.txt                    2022-02-02 18:45:22           14
```

By using the `--clear` option, you can clear an archive from path traversal payloads.

```console
[user@host ~]$ slipit --clear example.zip 
[user@host ~]$ slipit example.zip 
File Name                                             Modified             Size
example/                                       2022-02-02 18:39:00            0
example/images/                                2022-02-02 18:40:16            0
example/images/holiday.png                     2022-02-02 18:40:06        34001
example/images/beach.png                       2022-02-02 18:40:16         2112
example/documents/                             2022-02-02 18:39:48            0
example/documents/invoice.docx                 2022-02-02 18:39:40         3001
example/documents/important.docx               2022-02-02 18:39:48          121
```

*slipit* also allows to create an archive containing multiple payloads by using the `--multi` option:

```console
[user@host ~]$ slipit example.zip test.txt --static content --multi
[user@host ~]$ slipit example.zip 
File Name                                             Modified             Size
C:\Windows\test.txt                            2022-02-03 09:35:28            7
\\10.10.10.1\share\test.txt                    2022-02-03 09:35:28            7
/root/test.txt                                 2022-02-03 09:35:28            7
../test.txt                                    2022-02-03 09:35:28            7
..\test.txt                                    2022-02-03 09:35:28            7
../../test.txt                                 2022-02-03 09:35:28            7
..\..\test.txt                                 2022-02-03 09:35:28            7
../../../test.txt                              2022-02-03 09:35:28            7
..\..\..\test.txt                              2022-02-03 09:35:28            7
../../../../test.txt                           2022-02-03 09:35:28            7
..\..\..\..\test.txt                           2022-02-03 09:35:28            7
../../../../../test.txt                        2022-02-03 09:35:28            7
..\..\..\..\..\test.txt                        2022-02-03 09:35:28            7
```


### Supported Archive Types

----

Currently, the following archive types are supported (just naming their most common extension):

* `.zip`
* `.tar`
* `.tar.gz`
* `.tar.bz2`
