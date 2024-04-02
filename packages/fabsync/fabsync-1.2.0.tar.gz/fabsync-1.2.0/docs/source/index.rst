.. vim: set tw=80 lbr:

.. role:: python(code)
   :language: python

.. role:: toml(code)
   :language: toml


fabsync
=======

This is a file-syncing tool for `Fabric`_. It's almost as straightforward to
use as rsync, but with some of the features that will be familiar from
deployment automation tools like Ansible.

.. _Fabric: https://www.fabfile.org/

Source files are kept in a local file tree—presumably under source control—in
the same shape as the destination. The root of your local tree doesn't have to
correspond to the root directory (/) on the server, although that's the most
straightforward.

In addition to simply uploading files and directories with Fabric, fabsync has a
mechanism to configure metadata for the files, which comes in handy for
specifying ownership and permissions. You can also override the remote name, for
example to upload 'dot-local' as '.local'. And there's a mechanism to pass a
file's content through a rendering function, giving you a hook to integrate a
template system or any other kind of transformation you would like.

Locally, fabsync requires Python 3.8 or later. It's designed to work with pretty
much any POSIX remote host, using standard tools like ``sh``, ``getent`` and
``openssl``. If you find a BSD, GNU, or similar system that doesn't have the
tools we expect, reach out or send a patch.

The end of this document has an API reference, including a fully annotated
sample config. Following is a step-by-step guide to the available features.


Start
-----

We'll start with the simplest possible fabric task using fabsync. Suppose your
repo looks like this:

.. code-block:: text

   .
   ├── files
   │   └── etc
   │       └── lighttpd.conf
   └── fabfile.py

.. code-block:: python
   :caption: fabfile.py

   from fabric import task
   import fabsync

   @task
   def sync(conn):
       root = fabsync.load('files', '/')

       for result in fabsync.isync(conn, root):
           print(f"{result.path}{' [modified]' if result.modified else ''}")

Running this task will be roughly equivalent to running:

.. code-block:: sh

   rsync -rv files/ host:/


Metadata
--------

This isn't very useful yet, so let's add some metadata.

.. code-block:: text

   .
   ├── files
   │   ├── etc
   │   │   └── lighttpd.conf
   │   └── var
   │       └── www
   │           └── _sync.toml
   └── fabfile.py

.. code-block:: toml
   :caption: files/var/www/_sync.toml

   user = 'root'
   group = 'www'
   perms = 0o750

:ref:`sync-toml` has configuration for its parent directory and all of its
files. For the moment, we're only configuring ``/var/www`` with ownership and
permissions.

``user`` and ``group`` values can be either strings or numeric uid/gid values.
``perms`` is an integer, usually expressed in octal. All three can be ``-1``
(the default), which means to leave it as is.


Files
-----

Each :ref:`sync-toml` is also used to configure the files in the same directory.
A file's config goes in ``files.<filename>``, using the name in the local file
tree, not the name of the remote file. Usually these are the same, but you can
override the remote name, such as to more easily manage dot-files.

.. code-block:: text

   .
   ├── files
   │   └── home
   │       └── hg
   │           ├── _sync.toml
   │           └── dot-hgrc
   └── fabfile.py

.. code-block:: toml
   :caption: files/home/hg/_sync.toml

   # Options for /home/hg
   user = 'hg'
   group = 'hg'
   perms = 0o755

   # Options for /home/hg/.hgrc
   [files.'dot-hgrc']
   name = '.hgrc'
   user = 'hg'
   group = 'hg'
   perms = 0o640


Defaults
--------

The previous example has some duplication in it, which we can resolve. Every
:ref:`sync-toml` file can have a ``[defaults]`` section, which applies to the
current directory and everything underneath it (recursively). As the name
implies, these are just defaults, which can be overridden by options further
down the heirarchy.

.. code-block:: text

   .
   ├── files
   │   └── home
   │       └── hg
   │           ├── _sync.toml
   │           └── dot-hgrc
   └── fabfile.py

.. code-block:: toml
   :caption: files/home/hg/_sync.toml

   # Options for /home/hg
   perms = 0o755

   # Defaults for /home/hg and everything under it
   [defaults]
   user = 'hg'
   group = 'hg'
   dir_perms = 0o750
   file_perms = 0o640

   # Options for /home/hg/.hgrc
   [files.'dot-hgrc']
   name = '.hgrc'


Selection
---------

In many cases, it's sensible and safe to just sync your entire tree to apply any
changes. If you want to save a little time or just be absolutely sure that
you're only touching one thing, the :func:`~fabsync.isync` API takes an optional
:class:`~fabsync.ItemSelector` argument to filter the items.

:class:`~fabsync.ItemSelector` can limit the sync to specific subtree and/or to
a set of tags. We'll update our task to support these. While we're at it, we'll
add support for :func:`~fabsync.isync`'s ``dry_run`` parameter.

.. code-block:: python
   :caption: fabfile.py

   from fabric import task
   import fabsync

   @task(iterable=['tag'])
   def sync(conn, subpath=None, tag=(), dry_run=False):
       root = fabsync.load('files', '/')
       selector = fabsync.ItemSelector.new(subpath, tag)

       for result in fabsync.isync(conn, root, selector, dry_run=dry_run):
           print(f"{result.path}{' [modified]' if result.modified else ''}")

Tags are assigned to directories and files in :ref:`sync-toml`. They can also be
added to ``[defaults]`` sections to apply to a whole subtree. Tags accumulate,
so defining tags at a given level adds them to any existing tags that were
inherited. A tag can be removed by prepending a hyphen. Adding ``'-'`` as a tag
will reset, removing all inherited tags.

.. code-block:: text

   .
   ├── files
   │   ├── etc
   │   │   ├── _sync.toml
   │   │   └── lighttpd.conf
   │   ├── var
   │   │   └── www
   │   │       └── _sync.toml
   │   └── home
   │       └── hg
   │           ├── _sync.toml
   │           └── dot-hgrc
   └── fabfile.py

.. code-block:: toml
   :caption: files/etc/_sync.toml

   [files.'lighttpd.conf']
   tags = ['www']

.. code-block:: toml
   :caption: files/var/www/_sync.toml

   [defaults]
   user = 'root'
   group = 'www'
   file_perms = 0o640
   dir_perms = 0o750
   tags = ['www']

.. code-block:: toml
   :caption: files/home/hg/_sync.toml

   perms = 0o755

   [defaults]
   user = 'hg'
   group = 'hg'
   dir_perms = 0o750
   file_perms = 0o640
   tags = ['hg']

   [files.'dot-hgrc']
   name = '.hgrc'

To just sync ``/home/hg``, you might run either:

.. code-block:: sh

   fab sync --subpath home/hg

or:

.. code-block:: sh

   fab sync --tag hg

By default, :class:`~fabsync.ItemSelector` will automatically select the parents
of all selected items. In this example, neither the subpath nor the tag matches
``/home``, but because ``/home/hg`` is synced, ``/home`` is as well. You can
disable this behavior with :python:`ItemSelector.new(..., with_parents=False)`.


Rendering
---------

Some files need to be rendered at sync time, perhaps to customize them for a
specific host or to embed secrets from outside source control. To this end, any
file can be configured with a renderer, which is simply a function that takes
the :class:`~pathlib.Path` of the source file plus any configured render vars
and returns a new :class:`str` or :class:`bytes` with the final contents. The
default (trivial) renderer looks like this:

.. code-block:: python

   def renderer(path: Path, _vars: Mapping[str, Any], **kwargs) -> bytes:
       with path.open('rb') as f:
           return f.read()

Custom renderers can be hooked up to a template engine, Python string
formatting, or any other transformation that you want. If a string is returned,
it will be encoded as utf-8 for uploading.

Note that all renderers should include ``**kwargs`` in their argument list for
forward compatibility. As of version 1.2, legacy renderers with just the two
positional arguments are supported with a deprecation warning.

In :ref:`sync-toml`, the renderer is specified as an arbitrary string. At sync
time, you need to provide a mapping from these strings to the functions that
implement them. (Renderer names beginning with ``'fabsync/'`` are reserved and
can not be registered). The ``renderer`` key is valid for individual files and
also in the ``[defaults]`` section. You can also supply a mapping of arbitrary
values to parameterize the render function.

.. code-block:: text

   .
   ├── files
   │   └── etc
   │       ├── _sync.toml
   │       └── aliases
   └── fabfile.py

.. code-block:: toml
   :caption: files/etc/_sync.toml

   [files.'aliases']
   renderer = 'mako'
   vars = {'postmaster': 'alice@example.com'}

Individual vars can be overidden at each configuration level. Values are not
merged recursively.

It's likely that you'll want to load a render context once at the beginning of
the sync operation and reuse it for each file. Here's an example of what this
might look like:

.. code-block:: python
   :caption: fabfile.py

   import io
   from pathlib import Path
   import tomli
   from typing import Mapping, Any
   from fabric import task
   from mako.template import Template
   import fabsync

   def mako_renderer(conn):
       # Load some host-specific template context.
       result = conn.get('/usr/local/etc/fabsync.toml', io.BytesIO())
       host = tomli.loads(result.local.getvalue().decode())

       def render(path: Path, vars: Mapping[str, Any], **kwargs) -> str:
           return Template(filename=str(path)).render(host | vars)

       return render

   @task(iterable=['tag'])
   def sync(conn, subpath=None, tag=(), dry_run=False):
       root = fabsync.load('files', '/')
       selector = fabsync.ItemSelector.new(subpath, tag)
       renderers = {'mako': mako_renderer(conn)}

       for result in fabsync.isync(conn, root, selector, renderers, dry_run=dry_run):
           print(f"{result.path}{' [modified]' if result.modified else ''}")


Advanced Rendering
~~~~~~~~~~~~~~~~~~

.. versionadded:: 1.2

Render functions are given one additional keyword argument: ``get_content``.
This is a thunk (a zero-argument function) that will return the current (remote)
content of the file as a ``bytes`` object. This can be used by renderers that
wish to inspect and modify an existing file rather than simply create/overwrite
it. In this case, the source file could contain information you wish to merge
into the target or it might simply be an empty placeholder file to trigger the
renderer.

As a convenience, there is a special builtin renderer called ``fabsync/py`` that
will load a source file as a Python module, look for a function named
``render``, and call it as the render function. For example:

.. code-block:: toml
   :caption: _sync.toml

   [files.'rc.conf.py']
   name = 'rc.conf'
   renderer = 'fabsync/py'

.. code-block:: python
   :caption: rc.conf.py

   import re

   def render(_src, _vars, get_content, **kwargs) -> bytes:
       content = get_content()

       content = re.sub(rb'^pf_enable=.*$', b'pf_enable="YES"', content, flags=re.M)
       content = re.sub(rb'^jail_enable=.*$', b'jail_enable="YES"', content, flags=re.M)
       content = re.sub(rb'^sendmail_enable=.*$', b'sendmail_enable="NO"', content, flags=re.M)

       return content

Diffs
-----

By default, any time we decide to upload a file, we generate a diff of the
original and uploaded content. This is included in the
:class:`~fabsync.SyncResult` objected returned by :func:`~fabsync.isync`. This
is particularly useful when combined with the ``dry_run`` paramter:

.. code-block:: python

   @task(iterable=['tag'], incrementable=['verbose'])
   def sync(conn, subpath=None, tag=(), dry_run=False, verbose=0):
       root = fabsync.load('files', '/')
       selector = fabsync.ItemSelector.new(subpath, tag)

       for result in fabsync.isync(conn, root, selector, dry_run=dry_run):
           print(f"{result.path}{' [modified]' if result.modified else ''}")
           if verbose > 0 and result.diff:
               print(result.diff.decode())

Although the diff is provided as a :class:`bytes` object, it is a standard
unified diff similar to what you would get from ``/usr/bin/diff`` or a version
control system. We use :func:`difflib.diff_bytes` to avoid any unneccessary
assumptions about file encodings.

If you have any files that should not be diffed—perhaps because they are not
text files—you can set :toml:`diff = false` as a file or default option in
:ref:`sync-toml`.


Inspection
----------

:mod:`fabsync.files` has a few additional convenience functions for inspecting
your configuration. The most important is :func:`fabsync.files.table`, which
will generate human-readable table rows describing your file tree. Your
corresponding invoke task might look something like this:

.. code-block:: python

   import fabsync
   from invoke import task
   from prettytable import PrettyTable

   @task(iterable=['tag'])
   def table(c, subpath=None, tag=None):
       root = fabsync.files.load('files', '/')
       selector = fabsync.ItemSelector.new(subpath, tag)
       items = fabsync.files.select(root, selector)
       rows = fabsync.files.table(items)

       table = PrettyTable()
       table.align = 'l'
       table.field_names = next(rows)
       table.add_rows(rows)

       print(table)

Of course, you could also dump it to JSON and inspect it with `VisiData`_, or
anything else you like.

.. _VisiData: https://www.visidata.org/

The API reference below documents a few other functions for extracting
information from your sources.

Tips and tricks
---------------

Symlinks
~~~~~~~~

Symlinks in the source tree are followed normally. Symlinks on the server are
treated as symlinks rather than files or directories. Because we only sync files
and directories, this means that trying to sync anything over a symlink will be
treated as a type mismatch and raise a :class:`~fabsync.SyncError`.

The upshot is that fabsync can only be used to manage normal files and
directories. If you want symlinks on the remote host, you'll need some other
mechanism to manage them (not excluding just setting them up manually).

Because every file and directory will have a canonical link-free path, that's
the one you need to target. For example, if your system has ``/home ->
/usr/home``, you just need to sync ``/usr/home``.

Shared templates
~~~~~~~~~~~~~~~~

Combining a few of the above features, you can sync a single template to
multiple paths with different render vars. This example has config files for two
instances of an application. ``myapp.cfg`` is the shared template, which is not
synced. The actual files are local symlinks, which get rendered with different
parameters.

.. code-block:: text

    files
    └── usr
        └── local
            └── etc
                └── myapp
                    ├── _sync.toml
                    ├── myapp.cfg
                    ├── myapp1.cfg -> myapp.cfg
                    └── myapp2.cfg -> myapp.cfg

.. code-block:: toml
   :caption: usr/local/etc/myapp/_sync.toml

   [defaults]
   renderer = 'mako'

   # This is just the template.
   [files.'myapp.cfg']
   ignore = true

   [files.'myapp1.cfg'.vars]
   db.name = 'myapp1'
   http.port = 8000

   [files.'myapp2.cfg'.vars]
   db.name = 'myapp2'
   http.port = 8001

Looping
~~~~~~~

Because items are mapped one to one from source to destination, there's no
direct way to loop over a data structure and use that to create a file list. If
you're doing this a lot, you might want to ask whether fabsync is the right tool
for you.

That said, I'll reiterate one of the fundamental principles of fabsync: it's a
library, not a framework. You can call :func:`~fabsync.isync` as many times as
you want in any way you want to accomplish the task at hand. You can have
multiple source trees, one of which you sync repeatedly with different
destinations and/or render vars. You could generate a source tree into a temp
directory and sync that.

And, of course, you can always just use your Fabric connection to manipulate the
remote host directly. fabsync is a tool to be used where it's appropriate or
convenient, and ignored otherwise.

Local operation
~~~~~~~~~~~~~~~

Everything so far has been about syncing files to remote hosts, which is the
primary intention of fabsync. However, if you pass an :class:`invoke.Context` to
the sync API instead of a :class:`fabric.Connection`, it will manipulate the
local filesystem.


Reference
---------

Loading sources
~~~~~~~~~~~~~~~

.. autofunction:: fabsync.load

.. autoclass:: fabsync.ItemSelector
   :members:

.. class:: fabsync.files.SyncedRoot

   The root of a loaded source tree. This is a subclass of
   :class:`~fabsync.files.SyncedItem`.


Syncing
~~~~~~~

.. autofunction:: fabsync.isync

.. autofunction:: fabsync.sync

.. class:: fabsync.SyncResult

   The result of syncing a single item.

   .. attribute:: path
      :type: ~pathlib.PurePath

      The full path of the item on the remote host.

   .. attribute:: created
      :type: bool

      True if this item was created.

   .. attribute:: modified
      :type: bool

      True if this item was created or modified in any way.

   .. attribute:: diff
      :type: bytes

      A diff of the original and uploaded content, if applicable.

   .. attribute:: item
      :type: ~fabsync.files.SyncedItem

      The item that was synced.

Errors and validation
~~~~~~~~~~~~~~~~~~~~~

.. autoexception:: fabsync.config.ConfigError

.. autoexception:: fabsync.SyncError

.. autodata:: fabsync.config.schema
   :no-value:


Inspection
~~~~~~~~~~

These are functions that can help you inspect your configuration.

.. autofunction:: fabsync.files.table

.. autoclass:: fabsync.files.TableRow
   :members:
   :undoc-members:

.. autofunction:: fabsync.files.renderers

.. autofunction:: fabsync.files.tags


Lower-level utilities
~~~~~~~~~~~~~~~~~~~~~

Additional functions available for investigating the source tree.

.. autofunction:: fabsync.files.walk

.. autofunction:: fabsync.files.select

.. class:: fabsync.files.SyncedItem

   A file or directory loaded from the source tree.

   .. attribute:: src
      :type: ~pathlib.Path

      The local path to the file or directory.

   .. attribute:: dest
      :type: ~pathlib.PurePath

      The remote (target) path of the file or directory.

   .. attribute:: opts
      :type: ~fabsync.config.Opts

      Metadata and configuration.

   .. attribute:: children
      :type: dict[str, ~fabsync.files.SyncedItem]

      A map of (local) file and directory names to items directly underneath
      it.

.. autoclass:: fabsync.config.Opts
   :members:


.. _sync-toml:

_sync.toml
~~~~~~~~~~

Every directory in the source tree may have a ``_sync.toml`` to add configuration
and metadata.

.. code-block:: toml

   # Keys at the top level of _sync.toml pertain to the immediate parent
   # directory.

   # Override the name of this directory. The default is to use the local name
   # on disk. This must be a valid non-special file system name. In other
   # words, no path separators and you can't use '.' or '..'. If you manage to
   # do something sneaky with this, I don't want to hear your tale of woe.
   name = 'etc'

   # The user and group of this directory. These can be names or uid/gid
   # numbers. Set to -1 (the default) to leave them unspecified.
   user = 'root'
   group = 0

   # Permissions for chmod. This must be an integer, usually expressed in
   # octal. Set to -1 (the default) to leave it unspecified.
   perms = 0o755

   # Directories and files can be tagged so that you can sync a specific
   # subset of the tree. Tags accumulate, so this adds 'tag1' to any tags that
   # were inherited from a [defaults] section. Tags can be removed with a
   # hyphen prefix. A tag of '-' removes all inherited tags.
   tags = ['tag1', '-tagX']

   # Directories (and files) can be ignored. This is useful in rare cases and can
   # serve as an escape hatch if you need to hide one or more files temporarily
   # without removing them from version control. Ignoring a directory prunes the
   # entire subtree.
   ignore = false

   # Settings for files in this directory. Keys are (local) file names and
   # values are maps like the top level of this config. Note that these apply
   # to files only: entries for child directories are ignored.
   [files]
   'pf.conf' = { user = 'root', group = 0, perms = 0o640 }
   dot-something = { name = '.something' }

   # Naturally, you can also give files their own sections. Filenames with dots
   # (probably most of them) will of course need to be quoted.
   [files.'sudoers']
   user = 0
   group = 'wheel'
   perms = 0o440
   tags = ['-', 'tag3']
   ignore = false

   # When we upload a file, we normally provide a diff of the changes. If you
   # have files that can't or shouldn't be diffed, you can disable this.
   diff = false

   # Files can be passed through a rendering function before being uploaded.
   # This is just an arbitrary name; when syncing, you'll need to supply a
   # dictionary mapping your renderer names to actual functions.
   renderer = 'jinja2'

   # The render function will also receive a dictionary with file-specific
   # render context. Vars can also be added to [defaults] and will be
   # shallow-merged.
   [files.'sudoers'.vars]
   sudoers.alice = 'nopasswd'
   sudoers.bob = true

   # Settings that will serve as defaults for this directory and all
   # directories and files under it. Values are the same as above.
   [defaults]
   user = -1
   group = -1
   dir_perms = -1
   file_perms = -1
   tags = ['tag2']
   renderer = ''
   vars = {}
   diff = true


Change log
----------

.. toctree::
   :maxdepth: 1

   changes
