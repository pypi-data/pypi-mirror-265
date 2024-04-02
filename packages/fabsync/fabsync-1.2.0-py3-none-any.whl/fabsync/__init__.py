from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import difflib
from functools import cached_property, singledispatchmethod
import hashlib
import importlib.util
import inspect
import io
import os
from pathlib import Path, PurePath
import stat
from typing import Callable, Generator, Mapping, Optional, Union
import warnings

from .files import (
    ItemSelector,
    load,
    select,
    SyncedDir,
    SyncedFile,
    SyncedItem,
    SyncedRoot,
)
from .fs import FS, new_fs, SysInfo


Renderer = Callable[..., Union[str, bytes]]
Renderers = Mapping[str, Renderer]


__all__ = ['ItemSelector', 'load', 'isync', 'sync', 'SyncError']


class SyncError(Exception):
    """
    An unrecoverable error during sync.
    """


class SyncOpts:
    """
    A normalized :class:`~fabsync.config.Opts`.
    """

    uid: int = -1
    gid: int = -1
    perms: int = -1


class ItemSyncer(ABC):
    """
    Syncs one item to the server.

    This wrapper allows us to cache some values while we're processing this
    item.

    """

    item: SyncedItem

    def __init__(self, fs: FS, item: SyncedItem):
        self.fs = fs
        self.item = item

    def chown(self, uid: int, gid: int) -> None:
        self.fs.chown(self.target, uid, gid)
        self.reset()

    def chmod(self, perms: int) -> None:
        self.fs.chmod(self.target, perms)
        self.reset()

    @cached_property
    def stats(self) -> Optional[os.stat_result]:
        try:
            return self.fs.stat(self.target)
        except FileNotFoundError:
            return None

    def exists(self) -> bool:
        return self.stats is not None

    def matches_mode(self) -> bool:
        """
        True if the local and remote items have compatible filesystem types.

        This is trivially true if the remote item doesn't exist. Otherwise, we
        make sure that we're not trying to sync a file over a directory or vice
        versa.

        """
        stats = self.stats

        if stats is None:
            matches = True
        else:
            assert stats.st_mode is not None
            matches = self.item.matches_mode(stats.st_mode)

        return matches

    @abstractmethod
    def matches_content(self) -> bool:
        pass  # pragma: no cover

    @abstractmethod
    def diff(self) -> bytes:
        pass  # pragma: no cover

    @abstractmethod
    def put(self) -> None:
        pass  # pragma: no cover

    @cached_property
    def target(self) -> str:
        return str(self.item.dest)

    def reset(self):
        """
        Resets all cached attributes.
        """
        if 'stats' in self.__dict__:
            del self.stats


class DirSyncer(ItemSyncer):
    def matches_content(self) -> bool:
        """For a directory, 'content' is mere existence."""
        return self.stats is not None

    def diff(self) -> bytes:
        return b''

    def put(self) -> None:
        self.fs.mkdir(self.target)
        self.reset()


class FileSyncer(ItemSyncer):
    file: SyncedFile
    renderers: Renderers

    def __init__(self, fs: FS, file: SyncedFile, renderers: Renderers):
        self.file = file
        self.renderers = renderers

        super().__init__(fs, file)

    def matches_content(self) -> bool:
        if self.stats is None:
            matches = False
        elif len(self.content) != self.stats.st_size:
            matches = False
        else:
            new_md5 = hashlib.md5(self.content).digest()
            matches = new_md5 == self.md5

        return matches

    def diff(self) -> bytes:
        """A unified diff of the remote and local content."""
        if not self.file.opts.diff:
            return b''

        if self.exists():
            remote_lines = self.remote_content.splitlines(True)
        else:
            remote_lines = []
        local_lines = self.content.splitlines(True)

        try:
            path = self.file.dest.relative_to('/')
        except ValueError:
            path = self.file.dest

        diff_lines = difflib.diff_bytes(
            difflib.unified_diff,
            remote_lines,
            local_lines,
            fromfile=bytes(PurePath('a') / path),
            tofile=bytes(PurePath('b') / path),
        )

        return b''.join(diff_lines)

    def put(self) -> None:
        self.fs.put(io.BytesIO(self.content), self.target)
        self.reset()

    @cached_property
    def md5(self) -> bytes:
        """The current MD5 hash of the target, if any."""
        return self.fs.md5(self.target)

    @cached_property
    def remote_content(self) -> bytes:
        """
        The current remote content of the file.

        This will be an empty string if the file doesn't exist.

        """
        content = io.BytesIO()

        try:
            self.fs.get(self.file.dest, content)
        except FileNotFoundError:
            pass

        return content.getvalue()

    @cached_property
    def content(self) -> bytes:
        """The expected content of the file (after rendering)."""
        renderer: Renderer

        file = self.file

        key = file.opts.renderer
        if not key:
            renderer = self._read_file
        elif key == 'fabsync/py':
            renderer = self._render_py
        elif key.startswith('fabsync/'):
            raise SyncError(f"Renderer {key} is not defined.")
        elif key in self.renderers:
            renderer = self.renderers[key]
        else:
            raise SyncError(f"Renderer {key} is not configured.")

        if self._is_legacy_renderer(renderer):
            warnings.warn(
                f"Two-argument render functions are deprecated ({renderer.__module__}.{renderer.__qualname__}). Hint: add **kwargs.",
                DeprecationWarning,
                stacklevel=1,
            )
            content = renderer(file.src, file.opts.vars)
        else:
            content = renderer(
                file.src, file.opts.vars, get_content=lambda: self.remote_content
            )

        if isinstance(content, str):
            content = content.encode()

        return content

    @staticmethod
    def _read_file(src: Path, _vars, **kwargs) -> bytes:
        with src.open('rb') as f:
            content = f.read()

        return content

    @staticmethod
    def _render_py(
        src: Path, vars, get_content: Callable[[], bytes], **kwargs
    ) -> bytes:
        content: bytes

        if (
            spec := importlib.util.spec_from_file_location('renderer', src)
        ) and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
            except SyntaxError as e:
                raise SyncError(f"Failed to load {src} as a python module.") from e

            if hasattr(mod, 'render'):
                content = mod.render(src, vars, get_content=get_content)
            else:
                raise SyncError(f"{src} has no 'render' function.")
        else:  # pragma: no cover
            # This should be unreachable.
            raise SyncError(f"Failed to load {src} as a python module.")

        return content

    @staticmethod
    def _is_legacy_renderer(func: Callable) -> bool:
        param_kinds = tuple(
            param.kind for param in inspect.signature(func).parameters.values()
        )

        return param_kinds == (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )

    def reset(self) -> None:
        super().reset()

        if 'md5' in self.__dict__:
            del self.md5

        if 'remote_content' in self.__dict__:
            del self.remote_content


@dataclass(frozen=True)
class SyncResult:
    """
    The result of syncing a single item.
    """

    #: The item that was synced.
    item: SyncedItem

    #: True if the item was created.
    created: bool

    #: True if the path was modified in any way.
    modified: bool

    #: A unified diff, if this is a file that was uploaded.
    diff: bytes

    @property
    def path(self) -> PurePath:
        """The remote path, for convenience."""
        return self.item.dest


class Syncer:
    """
    Handles the syncing of individual files.

    This must be used as a context manager. Use one Syncer for a batch of
    files.

    """

    renderers: Renderers
    dry_run: bool
    no_chown: bool
    fs: FS
    sys: SysInfo

    def __init__(
        self,
        conn,
        renderers: Renderers,
        *,
        dry_run=False,
        no_chown=False,
    ):
        self.conn = conn
        self.renderers = renderers
        self.dry_run = dry_run
        self.no_chown = no_chown

    #
    # API
    #

    def sync(self, item: SyncedItem) -> SyncResult:
        assert not item.is_dest_root()

        if not hasattr(self, 'fs'):
            raise SyncError(
                f"{self.__class__.__name__} must be used as a context manager."
            )

        created = False
        modified = False
        diff = b''

        item_syncer = self._item_syncer(item)

        # Create the file or directory if it doesn't exist.
        if not item_syncer.matches_mode():
            raise SyncError(
                f"{item.src} (local) and {item.dest} (remote) are different types."
            )
        elif not item_syncer.matches_content():
            diff = item_syncer.diff()
            if not item_syncer.exists():
                created = True
            self._put(item_syncer)
            modified = True

        opts = self._item_sync_opts(item)
        stats = item_syncer.stats

        if stats is not None:
            if not self.no_chown:
                new_uid = opts.uid if (opts.uid >= 0) else (stats.st_uid or 0)
                new_gid = opts.gid if (opts.gid >= 0) else (stats.st_gid or 0)
                if (new_uid, new_gid) != (stats.st_uid, stats.st_gid):
                    self._chown(item_syncer, new_uid, new_gid)
                    modified = True

            perms = stat.S_IMODE(stats.st_mode or 0)
            if (opts.perms >= 0) and (opts.perms != perms):
                self._chmod(item_syncer, opts.perms)
                modified = True

        return SyncResult(item, created, modified, diff)

    #
    # Internal
    #

    @singledispatchmethod
    def _item_syncer(self, item: SyncedItem) -> ItemSyncer:
        raise TypeError(f"Unhandled item type: {item.__class__}.")  # pragma: no cover

    @_item_syncer.register
    def _(self, item: SyncedDir) -> ItemSyncer:
        return DirSyncer(self.fs, item)

    @_item_syncer.register
    def _(self, item: SyncedFile) -> ItemSyncer:
        return FileSyncer(self.fs, item, self.renderers)

    def _item_sync_opts(self, item: SyncedItem) -> SyncOpts:
        """
        Resolves item.opts into a SyncOpts.
        """
        opts = SyncOpts()

        opts.perms = item.opts.perms

        if isinstance(item.opts.user, str):
            try:
                opts.uid = self.sys.users[item.opts.user]
            except KeyError as e:
                raise SyncError(f"Unknown remote user: {item.opts.user}") from e
        else:
            opts.uid = item.opts.user

        if isinstance(item.opts.group, str):
            try:
                opts.gid = self.sys.groups[item.opts.group]
            except KeyError as e:
                raise SyncError(f"Unknown remote group: {item.opts.group}") from e
        else:
            opts.gid = item.opts.group

        return opts

    #
    # ItemSyncer wrappers
    #

    def _put(self, item_syncer: ItemSyncer) -> None:
        if not self.dry_run:
            item_syncer.put()

    def _chown(self, item_syncer: ItemSyncer, uid: int, gid: int) -> None:
        if not self.dry_run:
            item_syncer.chown(uid, gid)

    def _chmod(self, item_syncer: ItemSyncer, perms: int) -> None:
        if not self.dry_run:
            item_syncer.chmod(perms)

    #
    # Context manager
    #

    def __enter__(self) -> Syncer:
        self.fs = new_fs(self.conn)

        self.sys = self.fs.sysinfo()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.fs.cleanup()
        del self.fs


def isync(
    conn,
    root: SyncedRoot,
    selector: Optional[ItemSelector] = None,
    renderers: Optional[Renderers] = None,
    *,
    dry_run=False,
    no_chown=False,
) -> Generator[SyncResult, None, None]:
    """
    Synchronizes all or part of a local file tree with a remote host.

    This processes files and directories lazily, yielding each result before
    proceeding to the next item. This is useful for communicating results in
    real time as well as potentially terminating the process before the end.

    :param conn: Usually a Fabric connection. If this is an invoke Context,
        we'll operate locally instead.
    :type conn: ~fabric.connection.Connection

    :param root: The root of the tree to sync. Get this from
        :func:`fabsync.load`.
    :type root: ~fabsync.files.SyncedRoot

    :param selector: Optional parameters to select a
        subset of the tree to sync.
    :type selector: ~fabsync.ItemSelector

    :param dict renderers: Optional map of keys to render functions.

    :param bool dry_run: If true, we will inspect the remote system and report
        changes, but nothing will be modified.

    :param bool no_chown: If true, we will completely ignore file ownership.
        This is primarily useful in local mode, in which you likely don't have
        permission for :func:`os.chown`.

    :rtype: ~typing.Generator[SyncResult, None, None]

    """
    if selector is None:
        selector = ItemSelector()
    if renderers is None:
        renderers = {}

    with Syncer(conn, renderers, dry_run=dry_run, no_chown=no_chown) as syncer:
        for item in select(root, selector):
            if not item.is_dest_root():
                yield syncer.sync(item)


def sync(*args, **kwargs) -> dict[PurePath, SyncResult]:
    """
    Synchronizes all or part of a local file tree with a remote host.

    This is just a wrapper around :func:`isync` that gathers up all of the
    results to return at the end.

    :rtype: dict[~pathlib.PurePath, SyncResult]

    """
    results = {}
    for result in isync(*args, **kwargs):
        results[result.path] = result

    return results
