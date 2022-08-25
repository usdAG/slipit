from __future__ import annotations

import io
import tarfile
import fnmatch
from pathlib import Path
from slipit.archive_provider import ArchiveProvider


class TarProvider(ArchiveProvider):
    '''
    ArchiveProvider for tar files.
    '''
    def open(name: str) -> ArchiveProvider:
        '''
        Open the specified archive.

        Parameters:
            name            file system path of the archive

        Returns:
            ArchiveProvider for the opened archive
        '''
        tar_file = tarfile.open(name, 'a:')
        return TarProvider(tar_file)

    def create(name: str) -> ArchiveProvider:
        '''
        Create the specified archive.

        Parameters:
            name            file system path of the archive

        Returns:
            ArchiveProvider for the created archive
        '''
        tar_file = tarfile.open(name, 'w:')
        return TarProvider(tar_file)

    def append_file(self, filename: str, archived_name: str) -> None:
        '''
        Append a file to the archive.

        Parameters:
            filename            file system path to read the file from
            archived_name       file name within the archive

        Returns:
            None
        '''
        self.archive.add(filename, arcname=archived_name)

    def append_blob(self, blob: bytes, archived_name: str) -> None:
        '''
        Append a data blob to the archive.

        Parameters:
            blob                blob of bytes to append to the archive
            archived_name       file name within the archive

        Returns:
            None
        '''
        info = tarfile.TarInfo()

        info.type = tarfile.REGTYPE
        info.name = archived_name
        info.size = len(blob)

        file_like = io.BytesIO(blob)

        self.archive.addfile(info, file_like)

    def append_symlink(self, target: str, archived_name: str) -> None:
        '''
        Append a symlink to the archive.

        Parameters:
            target              symlink target
            archived_name       file name within the archive

        Returns:
            None
        '''
        info = tarfile.TarInfo()

        info.type = tarfile.SYMTYPE
        info.name = archived_name
        info.linkname = target

        self.archive.addfile(info, archived_name)

    def list_archive(name: str) -> None:
        '''
        Print a list of the archives content to stdout.

        Parameters:
            name            file system path of the archive

        Returns:
            None
        '''
        if not Path(name).is_file():
            raise FileNotFoundError(name)

        with tarfile.open(name, 'r:') as tar_file:
            tar_file.list()

    def remove_files(name: str, archived_name: str) -> None:
        '''
        Remove files matching the specified filename from the archive.

        Parameters:
            name            file system path of the archive
            archived_name   filename to match files against

        Returns:
            None
        '''
        TarProvider.remove_from_archive(name, archived_name, True)

    def clear_archive(name: str, payload: str) -> None:
        '''
        Clear the specified archive from path traversal sequences.

        Parameters:
            name            file system path of the archive
            payload         path traversal payload to look for

        Returns:
            None
        '''
        TarProvider.remove_from_archive(name, payload, False)

    def remove_from_archive(name: str, payload: str, use_fnmatch: bool) -> None:
        '''
        Remove all files matching the specified payload from the archive.
        The payload is either matched by using an 'in' statement on the
        archive filenames (use_fnmatch=False) or by using fnmatch
        (use_fnmatch=True).

        Parameters:
            name            file system path of the archive
            payload         payload to match filenames against
            fnmatch         whether to use fnmatch for matching

        Returns:
            None
        '''
        member_content_map = dict()

        if not Path(name).is_file():
            raise FileNotFoundError(name)

        with tarfile.open(name, 'r:') as tar_file:

            for member in tar_file.getmembers():

                if member.isfile():
                    content = tar_file.extractfile(member).read(member.size)
                    member_content_map[member] = io.BytesIO(content)

                else:
                    member_content_map[member] = None

        with tarfile.open(name, 'w:') as output:

            for member, content in member_content_map.items():

                if use_fnmatch and not fnmatch.fnmatch(member.name, payload):
                    output.addfile(member, content)

                if not use_fnmatch and payload not in member.name:
                    output.addfile(member, content)


for ext in ['.tar']:
    ArchiveProvider.register_provider_ext(TarProvider, ext)

for mime in ['application/x-tar', 'application/tar']:
    ArchiveProvider.register_provider_mime(TarProvider, mime)
