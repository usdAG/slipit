from __future__ import annotations


class ArchiveProvider:
    '''
    Interface class that provides methods for creating or appending to
    an archive.
    '''
    mime_type_providers = dict()
    file_extension_providers = dict()

    def __init__(self, archive) -> None:
        '''
        Initialize the provider with the archive it should use.

        Paramaters:
            archive         handle to the current archive
        '''
        self.archive = archive

    def open(name: str) -> ArchiveProvider:
        '''
        Open an existing archive.

        Parameters:
            name            filename of the archive to open

        Returns:
            None
        '''
        raise NotImplementedError

    def create(name: str) -> ArchiveProvider:
        '''
        Create an existing archive.

        Parameters:
            name            filename of the archive to create

        Returns:
            None
        '''
        raise NotImplementedError

    def append_file(self, filename: str, archived_name: str) -> None:
        '''
        Add an already existing file to the archive.

        Parameters:
            filename        file that is added to the archive
            archived_name   filename within the archive

        Returns:
            None
        '''
        raise NotImplementedError

    def append_files(self, filename: str, archived_names: [str]) -> None:
        '''
        Add an already existing file multiple times to the same archive,
        but use different archive names specified as list.

        Parameters:
            filename        file that is added to the archive
            archived_names  list of file names within the archive

        Returns:
            None
        '''
        for name in archived_names:
            self.append_file(filename, name)

    def append_blob(self, blob: bytes, archived_name: str) -> None:
        '''
        Append a data blob to the archive.

        Parameters:
            blob            blob of bytes to append to the archive
            archived_name   file name within the archive

        Returns:
            None
        '''
        raise NotImplementedError

    def append_blobs(self, blob: bytes, archived_names: [str]) -> None:
        '''
        Append a data blob to the archive under multiple different archive names.

        Parameters:
            blob            blob of bytes to append to the archive
            archived_names  list of file names within the archvie

        Returns:
            None
        '''
        for name in archived_names:
            self.append_blob(blob, name)

    def append_symlink(self, target: str, archived_name: str) -> None:
        '''
        Append a symlink to the archive.

        Parameters:
            target          symlink target
            archived_name   file name within the archive

        Returns:
            None
        '''
        raise NotImplementedError

    def append_symlinks(self, target: str, archived_names: [str]) -> None:
        '''
        Append a symlink to the archive with several different archive names.

        Parameters:
            target          symlink target
            archived_names  list of file names within the archvie

        Returns:
            None
        '''
        for name in archived_names:
            self.append_symlink(target, name)

    def remove_files(name: str, archived_name: str) -> None:
        '''
        Remove matching files from the archive.

        Parameters:
            name            file system path to the archive
            archived_name   filenames to remove from the archive

        Returns:
            None
        '''
        raise NotImplementedError

    def list_archive(name: str) -> None:
        '''
        Print a list of files contained within the archive.

        Parameters:
            name            file system path to the archive

        Returns:
            None
        '''
        raise NotImplementedError

    def clear_archive(name: str, payload: str) -> None:
        '''
        Clear the specified archive from path traversal sequences.

        Parameters:
            name            file system path of the archive
            payload         path traversal payload to look for

        Returns:
            None
        '''
        raise NotImplementedError

    def close_archive(self) -> None:
        '''
        Close the archive.

        Parameters:
            None

        Returns:
            None
        '''
        self.archive.close()

    def register_provider_ext(provider: ArchiveProvider, ext: str) -> None:
        '''
        Register an archive provider for the specified extension.

        Parameters:
            provider            ArchiveProvider to register
            ext                 file extension to register for

        Returns:
            None
        '''
        if ArchiveProvider.file_extension_providers.get(ext) is not None:
            raise ValueError(f"Provider for extension {ext} was already registered!")

        ArchiveProvider.file_extension_providers[ext] = provider

    def get_provider_ext(ext: str) -> ArchiveProvider:
        '''
        Return the ArchiveProvider that was registered for the specified file extension.

        Parameters:
            mime                file extension to get the provider for

        Returns:
            ArchiveProvider for the requested file extension
        '''
        return ArchiveProvider.file_extension_providers.get(ext)

    def register_provider_mime(provider: ArchiveProvider, mime: str) -> None:
        '''
        Register an archive provider for the specified mime type.

        Parameters:
            provider            ArchiveProvider to register
            mime                mime type to register the provider for

        Returns:
            None
        '''
        if ArchiveProvider.mime_type_providers.get(mime) is not None:
            raise ValueError(f"Provider for mime type {mime} was already registered!")

        ArchiveProvider.mime_type_providers[mime] = provider

    def get_provider_mime(mime: str) -> ArchiveProvider:
        '''
        Return the ArchiveProvider that was registered for the specified mime type.

        Parameters:
            mime                mime type to get the provider for

        Returns:
            ArchiveProvider for the requested mime type
        '''
        return ArchiveProvider.mime_type_providers.get(mime)
