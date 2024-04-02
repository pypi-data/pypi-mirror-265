from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque
import collections.abc
from dataclasses import dataclass
from functools import cached_property, singledispatch
from itertools import accumulate, chain
import os
from pathlib import Path, PurePath, PurePosixPath
import stat
from typing import (
    AbstractSet,
    cast,
    Iterable,
    Iterator,
    Mapping,
    NamedTuple,
    Optional,
    Union,
)

from .config import CONFIG_NAME, Opts, SyncConfig
from .functools import getitem


Children = Mapping[str, 'SyncedItem']


@singledispatch
def is_root_path(path: PurePath) -> bool:
    raise NotImplementedError()  # pragma: no cover


@is_root_path.register
def _(path: PurePosixPath) -> bool:
    return path == PurePosixPath('/')


class SyncedItem(ABC, collections.abc.Mapping):
    """
    A base class representing a synced file or directory.
    """

    # The local path of the file or directory.
    src: Path

    # The remote (target) path.
    dest: PurePath

    # Additional options.
    opts: Opts

    is_dir = False
    is_file = False

    def __init__(self, src: Path, dest: PurePath, opts: Opts):
        self.src = src
        self.dest = dest
        self.opts = opts

    @abstractmethod
    def matches_mode(self, mode: int) -> bool:
        pass  # pragma: no cover

    def is_dest_root(self):
        """True if this points to the root of the destination file system."""
        return is_root_path(self.dest)

    @property
    def children(self) -> Children:
        return {}

    def __getitem__(self, name: str) -> SyncedItem:
        return self.children[name]

    def __iter__(self):
        return iter(self.children.items())

    def __len__(self):
        return len(self.children)


class SyncedDir(SyncedItem):
    config: SyncConfig

    is_dir = True

    def __init__(
        self,
        src: Path,
        dest_dir: PurePath,
        parent_config: Optional[SyncConfig] = None,
    ):
        if parent_config is None:
            parent_config = SyncConfig.root()
            is_root = True
        else:
            is_root = False

        self.config = SyncConfig.load(src, parent_config.defaults, is_root=is_root)

        dest = dest_dir / self.config.name

        super().__init__(src, dest, self.config.dir_opts())

    def matches_mode(self, mode: int) -> bool:
        return stat.S_ISDIR(mode)

    def branch(self, path: Union[PurePath, str]) -> list[SyncedItem]:
        """
        Returns the list of items described by a relative path. Returns an
        empty list if any of the path components don't exist.

        :path: A relative path in the source tree.

        """
        if isinstance(path, str):
            path = PurePath(path)

        assert (
            not path.is_absolute()
        ), f"SyncedDir.find_branch() requires a relative path (got {path})."

        try:
            items = list(
                accumulate(path.parts, getitem, initial=cast(SyncedItem, self))
            )
        except KeyError:
            items = []

        return items

    def find(self, path: Union[PurePath, str]) -> Optional[SyncedItem]:
        """
        Returns the item identified by a relative path, if it exists.

        :path: A relative path in the source tree.

        """
        if branch := self.branch(path):
            return branch[-1]
        else:
            return None

    @cached_property
    def children(self) -> Children:
        children: dict[str, SyncedItem] = {}

        for child_src in sorted(self.src.iterdir()):
            if child_src.name == CONFIG_NAME:
                continue

            child: SyncedItem
            if child_src.is_dir():
                child = SyncedDir(child_src, self.dest, self.config)
            elif child_src.is_file():
                child = SyncedFile(
                    child_src,
                    self.dest,
                    self.config.file_opts(child_src.name),
                )
            else:
                raise IOError(
                    f"Can't process {child_src}: neither file nor directory."
                )  # pragma: no cover

            if not child.opts.ignore:
                children[child_src.name] = child

        return children


class SyncedFile(SyncedItem):
    is_file = True

    def __init__(self, src: Path, dest_dir: PurePath, opts: Opts):
        super().__init__(src, dest_dir / opts.name, opts)

    def matches_mode(self, mode: int) -> bool:
        return stat.S_ISREG(mode)


class SyncedRoot(SyncedDir):
    """
    The root of a SyncedItem hierarchy.
    """


@dataclass(frozen=True)
class ItemSelector:
    """
    Identifies a subset of items under a :class:`.SyncedRoot`.

    This essentially defines a filter to apply when traversing the source tree.
    The default values match all items.

    """

    #: A relative path into the source tree. We'll traverse the tree from
    #: this point. If the path isn't found, no items will be selected.
    subpath: Optional[PurePath] = None

    #: A set of tags to select. If empty, we will ignore tags. Otherwise, we'll
    #: only include items with at least one matching tag.
    tags: AbstractSet[str] = frozenset()

    #: If ``True`` (the default), we'll ensure that any time we select an item,
    #: all of its parent directories are selected as well. Thus, if you select
    #: a specific file—by path, tag, etc.—you're actually saying "select this
    #: item and all items necessary to reach it."
    with_parents: bool = True

    @classmethod
    def new(
        cls,
        subpath: Union[PurePath, str, None] = None,
        tags: Iterable[str] = (),
        with_parents=True,
    ) -> ItemSelector:
        """
        Creates a new :class:`ItemSelector`, with more flexible argument types.

        :param subpath:
        :type subpath: ~pathlib.PurePath or str or None

        :param tags:
        :type tags: ~typing.Iterable[str]

        :param bool with_parents:

        :rtype: ItemSelector

        """
        if isinstance(subpath, str):
            subpath = PurePath(subpath)
        tags = frozenset(tags)

        return cls(subpath, tags, with_parents)


def load(
    path: Union[Path, str],
    dest: Union[PurePath, str] = '/',
) -> SyncedRoot:
    """
    Loads a file tree for syncing.

    :param path: A path to the local file tree (usually relative).
    :type path: ~pathlib.Path or str

    :param dest: A remote path to sync to (usually absolute).
    :type dest: ~pathlib.PurePath or str

    :rtype: ~fabsync.files.SyncedRoot

    """
    if isinstance(path, str):
        path = Path(path)
    if isinstance(dest, str):
        dest = PurePath(dest)

    return SyncedRoot(path, dest)


def walk(top: SyncedItem) -> Iterator[SyncedItem]:
    """
    Generates a simple depth-first traversal of the items rooted at `top`.

    :param top: The starting point.
    :type top: ~fabsync.files.SyncedItem

    :rtype: ~typing.Iterator[~fabsync.files.SyncedItem]

    """
    yield top
    for child in top.children.values():
        yield from walk(child)


def select(root: SyncedRoot, selector: ItemSelector) -> Iterator[SyncedItem]:
    """
    Traverses the file tree, returning only items that match `selector`.

    :param root: The root from :func:`fabsync.load`.
    :type root: ~fabsync.files.SyncedRoot

    :param selector: Identifies items to include.
    :type selector: ~fabsync.ItemSelector

    :rtype: ~typing.Iterator[~fabsync.files.SyncedItem]

    """
    top: SyncedItem
    deferred: deque[SyncedItem] = deque()

    subpath = selector.subpath
    tags = selector.tags
    with_parents = selector.with_parents

    if subpath is not None:
        if branch := root.branch(subpath):
            top = branch[-1]
            if with_parents:
                deferred.extend(branch[:-1])
        else:
            return
    else:
        top = root

    for item in walk(top):
        if tags and not (tags & item.opts.tags):
            if with_parents and isinstance(item, SyncedDir):
                deferred.append(item)
            continue

        for d in deferred:
            if d.src in item.src.parents:
                yield d

        deferred.clear()

        yield item


class TableRow(NamedTuple):
    """
    Items generated by :func:`table`.

    Note that columns may be added in the future to include new features. Try
    not to make too many assumptions about this field list.

    """

    #: The local path
    src: str
    #: The remote path
    path: str
    #: User name or id
    user: str
    #: Group name or id
    group: str
    #: Mode
    mode: str
    #: Renderer name
    renderer: str
    #: Does this item support diffs?
    diff: str
    #: Space-separated tags
    tags: str


def table(
    items: Iterable[SyncedItem], header=True, relative_src=False
) -> Iterator[TableRow]:
    """
    A convenience function to generate human-readble data about items.

    This can be used to inspect your configuration by printing a table to the
    terminal or any other output format you find convenient.

    :param items: A collection of :class:`SyncedItem`, presumably from
        :func:`walk` or :func:`select`.
    :type items: ~typing.Iterable[SyncedItem]

    :param bool header: If ``True`` (the default), the first item will be a
        header row.
    :param bool relative_src: If ``True``, the ``src`` property of each row
        will be relative to the working directory.

    :rtype: ~typing.Iterator[TableRow]

    """
    if header:
        yield TableRow(
            "Source", "Path", "User", "Group", "Mode", "Renderer", "Diff?", "Tags"
        )

    for item in items:
        if item.is_dest_root():
            continue

        opts = item.opts

        mode = opts.perms
        if mode != -1:
            if item.is_dir:
                mode |= stat.S_IFDIR
            elif item.is_file:
                mode |= stat.S_IFREG

        src = item.src
        if relative_src:
            try:
                src = item.src.relative_to(os.getcwd())
            except ValueError:  # pragma: no cover
                pass

        yield TableRow(
            f"{src}{'/' if item.is_dir else ''}",
            f"{item.dest}{'/' if item.is_dir else ''}",
            str(opts.user) if opts.has_user() else "",
            str(opts.group) if opts.has_group() else "",
            stat.filemode(mode) if opts.has_perms() else "",
            opts.renderer,
            "no" if (item.is_file and not opts.diff) else "",
            " ".join(sorted(opts.tags)),
        )


def renderers(items: Iterable[SyncedItem]) -> frozenset[str]:
    """
    Returns the set of renderer names referenced by a collection of items.

    :param items: A collection of :class:`SyncedItem`, presumably from
        :func:`walk` or :func:`select`.
    :type items: ~typing.Iterable[SyncedItem]

    :rtype: frozenset[str]

    """
    return frozenset(
        filter(
            None,
            (item.opts.renderer for item in items),
        )
    )


def tags(items: Iterable[SyncedItem]) -> frozenset[str]:
    """
    Returns the set of tags referenced by a collection of items.

    :param items: A collection of :class:`SyncedItem`, presumably from
        :func:`walk` or :func:`select`.
    :type items: ~typing.Iterable[SyncedItem]

    :rtype: frozenset[str]

    """
    return frozenset(
        chain.from_iterable(
            (item.opts.tags for item in items),
        )
    )
