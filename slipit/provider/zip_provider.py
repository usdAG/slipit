from __future__ import annotations

import zipfile
from pathlib import Path
from slipit.archive_provider import ArchiveProvider


class ZipProvider(ArchiveProvider):
    '''
    ArchiveProvider for zip files.
    '''

    def open(name: str) -> ArchiveProvider:
        '''
        Open the specified archive.

        Parameters:
            name            file system path of the archive

        Returns:
            ArchiveProvider for the opened archive
        '''
        zip_file = zipfile.ZipFile(name, 'a')
        return ZipProvider(zip_file)

    def create(name: str) -> ArchiveProvider:
        '''
        Create the specified archive.

        Parameters:
            name            file system path of the archive

        Returns:
            ArchiveProvider for the created archive
        '''
        zip_file = zipfile.ZipFile(name, 'w')
        return ZipProvider(zip_file)

    def append_file(self, filename: str, archived_name: str) -> None:
        '''
        Append a file to the archive.

        Parameters:
            filename            file system path to read the file from
            archived_name       file name within the archive

        Returns:
            None
        '''
        self.archive.write(filename, archived_name)

    def append_blob(self, blob: bytes, archived_name: str) -> None:
        '''
        Append a data blob to the archive

        Parameters:
            blob                blob of bytes to append to the archive
            archived_name       file name within the archive

        Returns:
            None
        '''
        self.archive.writestr(archived_name, blob)

    def list_archive(name: str) -> None:
        '''
        Print a list of files contained within the archive.

        Parameters:
            name            file system path of the archive

        Returns:
            None
        '''
        if not Path(name).is_file():
            raise FileNotFoundError(name)

        with zipfile.ZipFile(name, 'r') as zip_file:
            zip_file.printdir()

    def clear_archive(name: str, payload: str) -> None:
        '''
        Clear the specified archive from path traversal sequences.

        Parameters:
            name            file system path of the archive
            payload         path traversal payload to look for

        Returns:
            None
        '''
        member_content_map = dict()

        if not Path(name).is_file():
            raise FileNotFoundError(name)

        with zipfile.ZipFile(name, 'r') as zip_file:

            for member in zip_file.infolist():

                if member.is_dir():
                    member_content_map[member] = ""

                else:
                    content = zip_file.open(member.filename).read()
                    member_content_map[member] = content

        with zipfile.ZipFile(name, 'w') as output:

            for member, content in member_content_map.items():

                if payload not in member.filename:
                    output.writestr(member, content)


for ext in ['.zip', '.jar', '.doc', '.docx']:
    ArchiveProvider.register_provider_ext(ZipProvider, ext)

for mime in ['application/zip', 'multipart/x-zip', 'application/x-zip-compressed', 'application/msword',
             'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
    ArchiveProvider.register_provider_mime(ZipProvider, mime)
