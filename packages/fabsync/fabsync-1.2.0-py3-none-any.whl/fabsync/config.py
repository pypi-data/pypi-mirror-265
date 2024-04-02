from __future__ import annotations

from collections import ChainMap
from dataclasses import dataclass, field
from pathlib import Path
from typing import AbstractSet, Any, cast, Mapping, MutableMapping, Union

from jsonschema import validate, ValidationError

from .functools import fnone, update_in


try:
    import tomllib as toml  # type: ignore[import]
except ModuleNotFoundError:
    import tomli as toml


#
# Constants and types
#

CONFIG_NAME = '_sync.toml'


Config = Mapping[str, Any]
Tags = AbstractSet[str]
Files = Mapping[str, Mapping[str, Any]]
User = Union[str, int]
Group = Union[str, int]
RenderVars = Mapping[str, Any]


#
# Validation tools
#

#: A JSON Schema describing the format of ``_sync.toml`` files.
schema: dict = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'allOf': [
        {'$ref': '#/$defs/entry'},
        {
            'properties': {
                'defaults': {
                    'type': 'object',
                    'properties': {
                        'user': {'$ref': '#/$defs/user_or_group'},
                        'group': {'$ref': '#/$defs/user_or_group'},
                        'dir_perms': {'$ref': '#/$defs/perms'},
                        'file_perms': {'$ref': '#/$defs/perms'},
                        'tags': {'$ref': '#/$defs/tags'},
                        'renderer': {'$ref': '#/$defs/renderer'},
                        'vars': {'$ref': '#/$defs/vars'},
                        'diff': {'type': 'boolean'},
                    },
                },
                'files': {
                    'type': 'object',
                    'propertyNames': {'$ref': '#/$defs/filename'},
                    'additionalProperties': {'$ref': '#/$defs/file'},
                },
            },
        },
    ],
    '$defs': {
        # Common properties that can be used at the top level or for an
        # individual file.
        'entry': {
            'properties': {
                'name': {'$ref': '#/$defs/filename'},
                'user': {'$ref': '#/$defs/user_or_group'},
                'group': {'$ref': '#/$defs/user_or_group'},
                'perms': {'$ref': '#/$defs/perms'},
                'tags': {'$ref': '#/$defs/tags'},
                'ignore': {'type': 'boolean'},
            },
        },
        # The value of an item in the 'files' map of a config.
        'file': {
            'type': 'object',
            'allOf': [
                {'$ref': '#/$defs/entry'},
                {
                    'properties': {
                        'renderer': {'$ref': '#/$defs/renderer'},
                        'vars': {'$ref': '#/$defs/vars'},
                        'diff': {'type': 'boolean'},
                    }
                },
            ],
        },
        'filename': {
            'allOf': [
                {'type': 'string'},
                {'not': {'pattern': r'/'}},
                {'not': {'enum': ['.', '..']}},
            ]
        },
        'user_or_group': {
            'anyOf': [
                {'type': 'string', 'pattern': r'^[a-z]+$'},
                {'type': 'integer', 'minimum': -1, 'maximum': 65535},
            ]
        },
        'perms': {
            'type': 'integer',
            'minimum': -1,
            'maximum': 0o777,
        },
        'tags': {
            'type': 'array',
            'items': {
                'type': 'string',
                'pattern': r'^[a-z-][a-z0-9_-]*$',
            },
        },
        'renderer': {
            'type': 'string',
        },
        'vars': {
            'type': 'object',
        },
    },
}


#
# Implementation
#


class ConfigError(Exception):
    """
    An error processing a _sync.toml file.
    """

    def __init__(self, msg: str, path: Path):
        super().__init__(msg)

        self.path = path


@dataclass
class Opts:
    """
    Normalized options for a file or directory.
    """

    #: The unqualified name of the item, used to build the remote path.
    name: str

    #: The user (name or ID) that should own this item.
    user: User = -1

    #: The group (name or ID) that should own this item.
    group: Group = -1

    #: The permissions to set.
    perms: int = -1

    #: Tags identifying this item for selection.
    tags: Tags = frozenset()

    #: The name of the renderer (ignored by directories).
    renderer: str = ''

    #: Additional context for the render function.
    vars: RenderVars = field(default_factory=dict)

    #: True if this file can be diffed (ignored by directories).
    diff: bool = True

    ignore: bool = False

    def has_user(self):
        return isinstance(self.user, str) or (self.user != -1)

    def has_group(self):
        return isinstance(self.group, str) or (self.group != -1)

    def has_perms(self):
        return self.perms != -1


class SyncConfig:
    """
    The configuration for a directory and its files.
    """

    # The raw config loaded from _sync.toml (or an emtpy map).
    config: Config

    # The default opts at this level, including any that we inherited.
    defaults: ChainMap

    def __init__(self, config: Config, defaults: ChainMap):
        self.config = config
        self.defaults = defaults

    @classmethod
    def load(cls, path: Path, base_defaults: ChainMap, is_root=False) -> SyncConfig:
        """
        Loads the config for the directory at `path`.
        """
        config_path = path / CONFIG_NAME
        if config_path.is_file():
            config = cls._load_config(config_path)
        else:
            config = {}

        if local_defaults := config.get('defaults'):
            defaults = cls._push_defaults(local_defaults, base_defaults)
        else:
            defaults = base_defaults

        if is_root:
            config['name'] = ''
        else:
            config.setdefault('name', path.name)

        return cls(config, defaults)

    @classmethod
    def _push_defaults(cls, defaults: MutableMapping, parent: ChainMap) -> ChainMap:
        """
        Adds a layer of defaults to its parent.

        For simple values, ChainMap does all the work for us. A few keys have
        special merge behavior that we need to take care of.

        """
        # Tags are merged in a somewhat complicated manner described in the
        # documentation.
        update_in(defaults, ['tags'], cls._resolve_tags, parent['tags'])

        # Render vars are just handled as a nested ChainMap to allow one level
        # of shadowing.
        update_in(defaults, ['vars'], parent['vars'].new_child)

        return parent.new_child(defaults)

    @classmethod
    def _load_config(cls, path: Path) -> dict:
        config: dict

        with path.open('rb') as f:
            try:
                config = toml.load(f)
                validate(config, schema)
            except toml.TOMLDecodeError as e:
                raise ConfigError(f"{path} is not valid TOML", path) from e
            except ValidationError as e:
                raise ConfigError(f"{path} is not a valid _sync.toml", path) from e
            else:
                cls._normalize_config(config)

        return config

    @staticmethod
    def _normalize_config(config: dict) -> None:
        """
        Normalizes the raw config data in place.
        """
        to_frozenset = fnone(frozenset, ())

        # Convert all tags from lists to sets.
        update_in(config, ['tags'], to_frozenset)
        update_in(config, ['defaults', 'tags'], to_frozenset)
        for filename in config.get('files', {}):
            update_in(config, ['files', filename, 'tags'], to_frozenset)

    @staticmethod
    def _resolve_tags(new: Tags, base: Tags) -> Tags:
        """Applies tag inheritance rules"""
        if '-' in new:
            base = frozenset()

        to_add = frozenset(tag for tag in new if not tag.startswith('-'))
        to_del = frozenset(tag[1:] for tag in new if tag.startswith('-'))

        return (base | to_add) - to_del

    @classmethod
    def root(cls) -> SyncConfig:
        """
        A root config to serve as the base for all.
        """
        defaults = ChainMap(
            {
                'user': -1,
                'group': -1,
                'dir_perms': -1,
                'file_perms': -1,
                'tags': frozenset(),
                'renderer': '',
                'vars': ChainMap(),
                'diff': True,
            }
        )

        return cls({}, defaults)

    @property
    def name(self) -> str:
        return cast(str, self.config['name'])

    @property
    def files(self) -> Files:
        return self.config.get('files', {})

    def dir_opts(self) -> Opts:
        config = self.config

        return Opts(
            name=config['name'],
            user=config.get('user', self.defaults['user']),
            group=config.get('group', self.defaults['group']),
            perms=config.get('perms', self.defaults['dir_perms']),
            tags=self._resolve_tags(
                config.get('tags', frozenset()),
                self.defaults['tags'],
            ),
            renderer='',
            vars={},
            diff=False,
            ignore=config.get('ignore', False),
        )

    def file_opts(self, name: str) -> Opts:
        config = self.files.get(name, {})

        return Opts(
            name=config.get('name', name),
            user=config.get('user', self.defaults['user']),
            group=config.get('group', self.defaults['group']),
            perms=config.get('perms', self.defaults['file_perms']),
            tags=self._resolve_tags(
                config.get('tags', frozenset()),
                self.defaults['tags'],
            ),
            renderer=config.get('renderer', self.defaults['renderer']),
            vars=dict(self.defaults['vars'], **config.get('vars', {})),
            diff=config.get('diff', self.defaults['diff']),
            ignore=config.get('ignore', False),
        )
