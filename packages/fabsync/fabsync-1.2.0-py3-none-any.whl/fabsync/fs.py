from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatch
import grp
import hashlib
import io
import os
from pathlib import Path
import pwd
from typing import cast, Iterator, Mapping, Optional, Tuple, TYPE_CHECKING, Union

import fabric


Pathable = Union[os.PathLike, str]


if TYPE_CHECKING:  # pragma: no cover
    from paramiko.sftp_client import SFTPClient


@dataclass(frozen=True)
class SysInfo:
    """
    System information from the remote host.
    """

    users: Mapping[str, int]
    groups: Mapping[str, int]


class FS(ABC):  # pragma: no cover
    """
    A filesystem abstraction.

    This includes all of the high-level operations we perform on files and
    directories. It allows us to transparently support fabric connections,
    invoke contexts, and test environments.

    """

    @abstractmethod
    def cleanup(self) -> None:
        pass

    @abstractmethod
    def sysinfo(self) -> SysInfo:
        pass

    @abstractmethod
    def stat(self, path: Pathable) -> Optional[os.stat_result]:
        pass

    @abstractmethod
    def md5(self, path: Pathable) -> bytes:
        pass

    @abstractmethod
    def mkdir(self, path: Pathable) -> None:
        pass

    @abstractmethod
    def get(self, path: Pathable, dest: io.BufferedIOBase) -> None:
        pass

    @abstractmethod
    def put(self, source: io.BufferedIOBase, path: Pathable) -> None:
        pass

    @abstractmethod
    def chown(self, path: Pathable, uid: int, gid: int) -> None:
        pass

    @abstractmethod
    def chmod(self, path: Pathable, perms: int) -> None:
        pass


class LocalFS(FS):
    """
    Local filesystem operations.
    """

    def cleanup(self) -> None:
        pass

    def sysinfo(self) -> SysInfo:
        return SysInfo(
            users={pw.pw_name: pw.pw_uid for pw in pwd.getpwall()},
            groups={gr.gr_name: gr.gr_gid for gr in grp.getgrall()},
        )

    def stat(self, path: Pathable) -> Optional[os.stat_result]:
        return os.lstat(path)

    def md5(self, path: Pathable) -> bytes:
        h = hashlib.md5()
        with Path(path).open('rb') as f:
            while buf := f.read(10240):
                h.update(buf)

        return h.digest()

    def mkdir(self, path: Pathable) -> None:
        os.mkdir(path)

    def get(self, path: Pathable, dest: io.BufferedIOBase) -> None:
        with open(path, 'rb') as f:
            while buf := f.read(10240):
                dest.write(buf)

    def put(self, source: io.BufferedIOBase, path: Pathable) -> None:
        with open(path, 'wb') as f:
            while data := source.read(10240):
                f.write(data)

    def chown(self, path: Pathable, uid: int, gid: int) -> None:  # pragma: no cover
        os.chown(path, uid, gid)

    def chmod(self, path: Pathable, perms: int) -> None:
        os.chmod(path, perms)


@singledispatch
def new_fs(c) -> FS:
    return LocalFS()


class RemoteFS(FS):
    """
    Filesystem operations over a fabric connection.
    """

    MD5_PATH = '/tmp/fabsync-md5.sh'

    conn: fabric.Connection
    sftp: SFTPClient

    def __init__(self, conn: fabric.Connection):
        self.conn = conn
        self.sftp = conn.sftp()

        self._upload_helper()

    def _upload_helper(self):
        self.conn.put(str(Path(__file__).parent / 'md5.sh'), self.MD5_PATH)
        self.sftp.chmod(self.MD5_PATH, 0o700)

    def cleanup(self) -> None:
        self.sftp.unlink(self.MD5_PATH)

    def sysinfo(self) -> SysInfo:
        def entries(stdout: str) -> Iterator[Tuple[str, int]]:
            for row in stdout.splitlines():
                cols = row.split(':')
                yield cols[0], int(cols[2])

        users = self.conn.run('getent passwd', hide='both')
        groups = self.conn.run('getent group', hide='both')

        return SysInfo(
            users=dict(entries(users.stdout)), groups=dict(entries(groups.stdout))
        )

    def stat(self, path: Pathable) -> Optional[os.stat_result]:
        try:
            return cast(os.stat_result, self.sftp.lstat(os.fspath(path)))
        except FileNotFoundError:
            return None

    def md5(self, path: Pathable) -> bytes:
        result = self.conn.run(f'{self.MD5_PATH} {str(os.fspath(path))}', hide='both')
        md5 = bytes.fromhex(result.stdout.split()[0])

        return md5

    def mkdir(self, path: Pathable) -> None:
        self.sftp.mkdir(os.fspath(path))

    def get(self, path: Pathable, dest: io.BufferedIOBase) -> None:
        self.conn.get(path, dest)

    def put(self, source: io.BufferedIOBase, path: Pathable) -> None:
        self.conn.put(source, os.fspath(path), preserve_mode=False)

    def chown(self, path: Pathable, uid: int, gid: int) -> None:
        self.sftp.chown(os.fspath(path), uid, gid)

    def chmod(self, path: Pathable, perms: int) -> None:
        self.sftp.chmod(os.fspath(path), perms)


@new_fs.register
def _(c: fabric.Connection) -> RemoteFS:  # pragma: no cover
    return RemoteFS(c)
