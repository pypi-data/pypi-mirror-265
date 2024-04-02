from __future__ import annotations

from pathlib import Path, PurePath
from unittest import TestCase

from fabsync.files import (
    ItemSelector,
    load,
    renderers,
    select,
    SyncedItem,
    SyncedRoot,
    table,
    tags,
    walk,
)


dir_mode = 0x4755
file_mode = 0x8644


class FileTestCase(TestCase):
    root_name: str = ''

    def setUp(self):
        if name := self.root_name:
            self.root = load(Path(__file__).parent / 'files' / name)


class Loading(FileTestCase):
    root_name = 'loading'

    def test_parse(self):
        self.assertTrue(isinstance(self.root, SyncedRoot))
        self.assertTrue(self.root.is_dest_root())

    def test_load_str_paths(self):
        root = load(str(Path(__file__).parent / 'files/loading'), '/')

        self.assertTrue(isinstance(root, SyncedRoot))
        self.assertTrue(root.is_dest_root())

    def test_children(self):
        self.assertTrue(isinstance(self.root['dir1'], SyncedItem))
        self.assertEqual(len(self.root['dir1']), 1)
        self.assertEqual(len(list(self.root['dir1'])), 1)

    def test_dir(self):
        self.assertTrue(self.root.matches_mode(dir_mode))
        self.assertFalse(self.root.matches_mode(file_mode))

    def test_file(self):
        file = self.root['file1.txt']

        self.assertTrue(file.matches_mode(file_mode))
        self.assertFalse(file.matches_mode(dir_mode))
        self.assertEqual(file.children, {})
        self.assertFalse(file.opts.ignore)

    def test_branch(self):
        branch = self.root.branch(PurePath('dir1/file3.txt'))

        self.assertEqual(len(branch), 3)

    def test_branch_none(self):
        branch = self.root.branch(PurePath('dir1/bogus.txt'))

        self.assertEqual(len(branch), 0)

    def test_find(self):
        file = self.root.find(PurePath('dir1/file3.txt'))

        self.assertIsNotNone(file)
        self.assertEqual(file.src, self.root.src / 'dir1/file3.txt')

    def test_find_none(self):
        file = self.root.find('dir1/bogus.txt')

        self.assertIsNone(file)

    def test_opts_name(self):
        self.assertEqual(self.root.find('dot-config').opts.name, '.config')
        self.assertEqual(self.root.find('dot-profile').opts.name, '.profile')
        self.assertEqual(self.root.find('file1.txt').opts.name, 'file1.txt')

    def test_opts_owner(self):
        self.assertEqual(self.root.find('dot-config').opts.user, 1000)
        self.assertEqual(self.root.find('file1.txt').opts.user, -1)

    def test_opts_group(self):
        self.assertEqual(self.root.opts.group, 1000)
        self.assertEqual(self.root.find('file1.txt').opts.group, 1000)

    def test_opts_perms(self):
        self.assertEqual(self.root.opts.perms, 0o700)
        self.assertEqual(self.root.find('dot-profile').opts.perms, 0o600)
        self.assertEqual(self.root.find('file1.txt').opts.perms, 0o640)

    def test_ignore(self):
        self.assertIsNone(self.root.find('ignore-me/file.txt'))
        self.assertIsNone(self.root.find('dir1/ignore-me.txt'))

    def test_walk(self):
        paths = list(walk(self.root))

        self.assertEqual(len(paths), 8)

    def test_table(self):
        rows = list(table(walk(self.root)))

        self.assertEqual(len(rows), 8)

        rows = list(table(walk(self.root), relative_src=True))

        self.assertEqual(len(rows), 8)

        rows = list(table(select(self.root, ItemSelector()), header=False))

        self.assertEqual(len(rows), 7)

    def test_renderers(self):
        all_renderers = renderers(walk(self.root))

        self.assertEqual(all_renderers, {'rot13'})

    def test_tags(self):
        all_tags = tags(walk(self.root))

        self.assertEqual(all_tags, {'dot'})


class Selection(FileTestCase):
    root_name = 'selection'

    def test_select_default(self) -> None:
        selector = ItemSelector.new()
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 9)

    def test_select_all(self) -> None:
        selector = ItemSelector.new(subpath=None, tags=frozenset())
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 9)

    def test_select_none(self) -> None:
        selector = ItemSelector.new(subpath='home')
        items = list(select(self.root, selector))

        self.assertEqual(items, [])

    def test_select_deep(self) -> None:
        selector = ItemSelector.new(subpath='usr/local/bin/myapp.py')
        items = list(select(self.root, selector))

        src = self.root.src
        self.assertEqual(
            [item.src for item in items],
            [
                src,
                src / 'usr',
                src / 'usr/local',
                src / 'usr/local/bin',
                src / 'usr/local/bin/myapp.py',
            ],
        )

    def test_select_deep_only(self) -> None:
        selector = ItemSelector.new(
            subpath='usr/local/bin/myapp.py', with_parents=False
        )
        items = list(select(self.root, selector))

        src = self.root.src
        self.assertEqual(
            [item.src for item in items],
            [src / 'usr/local/bin/myapp.py'],
        )

    def test_select_etc(self) -> None:
        selector = ItemSelector.new(subpath=PurePath('etc'))
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 3)

    def test_select_etc_only(self) -> None:
        selector = ItemSelector.new(subpath=PurePath('etc'), with_parents=False)
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 2)

    def test_select_usr(self) -> None:
        selector = ItemSelector.new(subpath=PurePath('usr'))
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 5)

    def test_select_usr_only(self) -> None:
        selector = ItemSelector.new(subpath=PurePath('usr'), with_parents=False)
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 4)

    def test_select_pf(self) -> None:
        selector = ItemSelector.new(tags={'pf'})
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 3)

    def test_select_pf_only(self) -> None:
        selector = ItemSelector.new(tags=['pf'], with_parents=False)
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 1)

    def test_select_myapp(self) -> None:
        selector = ItemSelector.new(tags=['myapp'])
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 7)

    def test_select_myapp_only(self) -> None:
        selector = ItemSelector.new(tags=['myapp'], with_parents=False)
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 2)

    def test_select_tags_only(self) -> None:
        selector = ItemSelector.new(tags=['pf', 'myapp'], with_parents=False)
        items = list(select(self.root, selector))
        self.assertEqual(len(items), 3)

    def test_select_intersection(self) -> None:
        selector = ItemSelector.new(subpath='usr', tags=['pf'])
        items = list(select(self.root, selector))

        self.assertEqual(len(items), 0)
