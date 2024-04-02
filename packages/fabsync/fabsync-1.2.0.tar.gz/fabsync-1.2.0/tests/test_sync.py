from __future__ import annotations

from functools import cached_property
import io
import os
from pathlib import Path, PurePath
import shlex
import shutil
import subprocess
from tempfile import TemporaryDirectory
from typing import Mapping, Tuple, Union
from unittest import TestCase
from unittest.mock import patch
import warnings

import invoke

import fabsync
from fabsync import ItemSelector, Syncer, SyncError
from fabsync.fs import SysInfo


class TestFSMixin:
    def sysinfo(self) -> SysInfo:
        sysinfo = super().sysinfo()  # type: ignore[misc]

        return SysInfo(
            users=dict(sysinfo.users, hg=5000),
            groups=dict(sysinfo.groups, hg=5000),
        )


class TestLocalFS(TestFSMixin, fabsync.fs.LocalFS):
    pass


class TestRemoteFS(TestFSMixin, fabsync.fs.RemoteFS):
    pass


def slurp(path, vars, **kwargs):
    with path.open(mode='rb') as f:
        return f.read()


class SyncTestCase(TestCase):
    """
    Base class for sync tests.

    By default, this uses an invoke Context instead of a fabric Connection. All
    filesystem operations go through fabsync.fs.LocalFS, which just uses local
    APIs from the os module and similar. Ownership config is ignored, since you
    almost certainly don't have chown permissions.

    Toward the bottom is a set of tests using a mock fabric Connection to cover
    the fabric wrapper.

    """

    # A relative path under 'sync' for loading the local root.
    root_name = ''
    no_chown = True

    def setUp(self):
        # This will be the target of all sync operations.
        dir = TemporaryDirectory(dir='.')
        self.addCleanup(dir.cleanup)
        self.local_path = Path(dir.name)

        self.conn = self._new_connection()
        if name := self.root_name:
            self.root = fabsync.load(Path(__file__).parent / 'sync' / name, self.dest)

    @property
    def dest(self):
        """
        The second argument to fabsync.load.
        """
        return self.local_path

    def _new_connection(self):
        return invoke.Context()

    def sync(self, selector=None, renderers=None, dry_run=False):
        if renderers is None:
            renderers = {'test': slurp}

        return fabsync.sync(
            self.conn,
            self.root,
            selector,
            renderers,
            dry_run=dry_run,
            no_chown=self.no_chown,
        )


class Coverage(SyncTestCase):
    root_name = 'empty'

    def test_defaults(self):
        fabsync.sync(self.conn, self.root)

    def test_no_helper(self) -> None:
        syncer = Syncer(self.conn, {})

        with self.assertRaises(SyncError):
            syncer.sync(next(iter(self.root))[1])


class MissingRenderer(SyncTestCase):
    root_name = 'errors/render'

    def test_renderer_missing(self):
        with self.assertRaises(SyncError):
            self.sync(selector=ItemSelector.new(subpath='missing.txt'))

    def test_builtin_renderer_missing(self):
        """
        Renderers with the 'fabsync/' prefix are reserved and may not be
        defined.
        """
        with self.assertRaises(SyncError):
            self.sync(
                selector=ItemSelector.new(subpath='builtin.txt'),
                renderers={'fabsync/custom': lambda p, v: b''},
            )

    def test_bad_module(self):
        with self.assertRaises(SyncError):
            self.sync(selector=ItemSelector.new(subpath='bad_module.py'))

    def test_no_render_function(self):
        with self.assertRaises(SyncError):
            self.sync(selector=ItemSelector.new(subpath='no_render.py'))


class ModeMismatch(SyncTestCase):
    root_name = 'errors/mode'

    def test_dir_over_file(self):
        (self.local_path / 'etc').touch()

        with self.assertRaises(SyncError):
            self.sync()

    def test_file_over_dir(self):
        (self.local_path / 'var').mkdir()

        with self.assertRaises(SyncError):
            self.sync()


class MissingUser(SyncTestCase):
    root_name = 'errors/user'

    def test_missing_user(self):
        with self.assertRaises(SyncError):
            self.sync()


class MissingGroup(SyncTestCase):
    root_name = 'errors/group'

    def test_missing_user(self):
        with self.assertRaises(SyncError):
            self.sync()


class GeneralTests:
    """
    A mixin with general sync tests.
    """

    root_name = 'general'

    def test_dry_run_new(self):
        results = self.sync(dry_run=True)

        result = results[self.dest / 'home/hg/.hgrc']
        self.assertTrue(result.created)
        self.assertTrue(result.modified)
        self.assertNotEqual(result.diff, b'')
        self.assertFalse((self.local_path / 'home/hg/.hgrc').exists())

    def test_dry_run_existing(self):
        (self.local_path / 'home/hg/bin').mkdir(parents=True)
        (self.local_path / 'home/hg/bin/hook.sh').touch()

        results = self.sync(dry_run=True)

        result = results[self.dest / 'home/hg/bin/hook.sh']
        self.assertFalse(result.created)
        self.assertTrue(result.modified)
        self.assertNotEqual(result.diff, b'')

    def test_sync_new(self):
        results = self.sync()

        result = results[self.dest / 'home/hg/.hgrc']
        self.assertTrue(result.created)
        self.assertTrue(result.modified)
        self.assertNotEqual(result.diff, b'')
        self.assertEqual(
            (self.local_path / 'home/hg/.hgrc').read_text(),
            (self.root.src / 'home/hg/dot-hgrc').read_text(),
        )

    def test_sync_existing(self):
        (self.local_path / 'home/hg/bin').mkdir(parents=True)
        (self.local_path / 'home/hg/bin/hook.sh').touch()

        results = self.sync()

        path = self.dest / 'home/hg/bin/hook.sh'
        result = results[path]
        self.assertFalse(result.created)
        self.assertTrue(result.modified)
        self.assertNotEqual(result.diff, b'')
        self.assertEqual(
            (self.local_path / 'home/hg/bin/hook.sh').read_text(),
            (self.root.src / 'home/hg/bin/hook.sh').read_text(),
        )

    def test_sync_noop(self):
        selector = ItemSelector.new(subpath=PurePath('etc'))
        results = self.sync(selector=selector)
        results = self.sync(selector=selector)

        for result in results.values():
            with self.subTest(result.path):
                self.assertFalse(result.created)
                self.assertFalse(result.modified)
                self.assertEqual(result.diff, b'')

    def test_sync_py(self):
        dest_path = self.local_path / 'etc/rc.conf'
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, 'wt') as f:
            f.write('hostname="test"\npf_enable="NO"\njail_enable="YES"\n')

        results = self.sync()

        result = results[self.dest / 'etc/rc.conf']
        self.assertFalse(result.created)
        self.assertTrue(result.modified)
        self.assertNotEqual(result.diff, b'')
        self.assertEqual(
            dest_path.read_text(),
            'hostname="test"\npf_enable="YES"\njail_enable="YES"\n',
        )

    def test_content_check(self):
        def upper(path: Path, _vars: Mapping, **kwargs) -> str:
            with path.open('rt') as f:
                return f.read().upper()

        self.sync()
        results = self.sync(renderers={'test': upper})

        result = results[self.dest / 'home/hg/.hgrc']
        self.assertFalse(result.created)
        self.assertTrue(result.modified)
        self.assertNotEqual(result.diff, b'')
        self.assertEqual(
            (self.local_path / 'home/hg/.hgrc').read_text(),
            (self.root.src / 'home/hg/dot-hgrc').read_text().upper(),
        )

    def test_no_remote_content(self):
        with Syncer(self.conn, {}) as syncer:
            file = next(item for item in fabsync.files.walk(self.root) if item.is_file)
            item_syncer = syncer._item_syncer(file)
            content = item_syncer.remote_content

        self.assertEqual(content, b'')

    def test_deprecated_render_function(self):
        def renderer(path: Path, _vars: Mapping) -> bytes:
            with path.open('rb') as f:
                return f.read()

        with warnings.catch_warnings(record=True) as warns:
            self.sync(renderers={'test': renderer})
            self.assertEqual(len(warns), 1)
            self.assertEqual(warns[0].category, DeprecationWarning)


@patch('fabsync.fs.LocalFS', TestLocalFS)
class Local(GeneralTests, SyncTestCase):
    """
    General tests using fabsync.fs.LocalFS.
    """

    def test_mode(self):
        results = self.sync()

        path = self.dest / 'home/hg/bin/hook.sh'
        result = results[path]
        self.assertTrue(result.created)
        self.assertTrue(result.modified)
        self.assertEqual(os.lstat(path).st_mode, 0o100755)


class Remote(GeneralTests, SyncTestCase):
    """
    The general tests again, but with a mock Fabric connection.

    This covers fabsync.fs.RemoteFS.

    """

    no_chown = False

    @property
    def dest(self):
        return PurePath('/')

    def _new_connection(self):
        return TestConnection(self.local_path)

    def test_mode(self):
        results = self.sync()

        path = self.dest / 'home/hg/bin/hook.sh'
        result = results[path]
        self.assertTrue(result.created)
        self.assertTrue(result.modified)
        self.assertEqual(self.conn.sftp().own[str(path)], (5000, 5000))
        self.assertEqual(self.conn.mock_path(path).stat().st_mode, 0o100755)


#
# Util
#


class TestConnection:
    """
    A mock fabric connection.

    This takes a temporary directory to play the part of the remote filesystem.
    Methods map full paths into this space as necessary. Relative paths are
    left alone, but we really shouldn't be using them.

    """

    class SFTPClient:
        # A record of chown calls.
        own: dict[str, Tuple[int, int]]

        def __init__(self, root):
            self.root = root
            self.own = {}

        def chmod(self, path, mode):
            return os.chmod(mock_path(self.root, path), mode)

        def chown(self, path, uid, gid):
            self.own[path] = (uid, gid)

        def mkdir(self, path):
            return os.mkdir(mock_path(self.root, path))

        def lstat(self, path):
            return os.lstat(mock_path(self.root, path))

        def unlink(self, path):
            return os.unlink(mock_path(self.root, path))

    def __init__(self, local_path):
        self.root = local_path

        (self.root / 'tmp').mkdir()

    def mock_path(self, path):
        return mock_path(self.root, path)

    def get(self, remote, local):
        remote = self.mock_path(remote)

        if isinstance(local, (Path, str)):
            shutil.copyfile(remote, local)
        elif isinstance(local, io.IOBase):
            with remote.open('rb') as f:
                local.write(f.read())
        else:
            raise ValueError(local)

    def put(self, local, remote, preserve_mode=True):
        remote = self.mock_path(remote)

        if isinstance(local, (Path, str)):
            shutil.copyfile(local, remote)
        elif isinstance(local, io.IOBase):
            with remote.open('wb') as f:
                f.write(local.read())
        else:
            raise ValueError(local)

    def run(self, command, **kwargs):
        def map_path(arg: str) -> str:
            if arg.startswith('/'):
                arg = str(self.mock_path(arg))
            return arg

        args = [map_path(arg) for arg in shlex.split(command)]
        try:
            result = subprocess.run(args, capture_output=True, check=True)
        except FileNotFoundError:
            # Fake getent if necessary to allow the tests to run on macOS.
            if args[0] == 'getent' and args[1] in ['passwd', 'group']:
                result = subprocess.run(
                    ['grep', '-v', '^#', f'/etc/{args[1]}'],
                    capture_output=True,
                )
            else:
                raise

        return invoke.Result(result.stdout.decode())

    def sftp(self):
        return self._sftp

    @cached_property
    def _sftp(self):
        return self.SFTPClient(self.root)


@fabsync.fs.new_fs.register
def _(conn: TestConnection):
    return TestRemoteFS(conn)


def mock_path(root: Path, path: Union[PurePath, str]) -> Path:
    if isinstance(path, str):
        path = PurePath(path)
    if path.is_absolute():
        path = path.relative_to('/')

    return root / path
