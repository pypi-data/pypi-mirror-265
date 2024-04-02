<!-- vim: set tw=80 lbr: -->
# fabsync

- Homepage: https://sr.ht/~psagers/fabsync/
- Source code: https://hg.sr.ht/~psagers/fabsync
- Documentation: https://fabsync.ignorare.net/

## Overview

This is a file-syncing tool for [Fabric][]. It's almost as straightforward to
use as rsync, but with some of the features that will be familiar from
deployment automation tools like Ansible.

Key points:

- Source files are kept in a simple directory tree, as if you were going to
  rsync them.
- Metadata—such as ownership and permissions—is configured in TOML files
  throughout the tree.
- Rendering functions can be configured to transform file contents. You can hook
  these up to template engines or anything else.
- Paths and tags can be used to sync a subset of the file tree.

The most important thing to note is that this is a library, not a framework. It
does one simple thing, which you're welcome to integrate into your own
deployment scheme any way you like. For illustration purposes, here's a fragment
of a hypothetical `fabfile.py` that you might write:

```python
import io
from pathlib import Path
from typing import Any, Mapping

from fabric import Connection, task
import fabsync
import pystache
import tomli


def _mustache_renderer(conn: Connection) -> fabsync.Renderer:
    try:
        result = conn.get('/usr/local/etc/fabsync.toml', io.BytesIO())
    except FileNotFoundError:
        host = {}
    else:
        host = tomli.loads(result.local.getvalue().decode())

    renderer = pystache.Renderer(escape=lambda s: s)

    def render(path: Path, vars: Mapping[str, Any]) -> str:
        with path.open('rt') as f:
            return renderer.render(f.read(), host | vars)

    return render


@task(iterable=['tag'], incrementable=['verbose'])
def sync(conn, subpath=None, tag=None, verbose=0):
    root = fabsync.load('files', '/')
    selector = fabsync.ItemSelector.new(subpath=subpath, tags=tag)
    renderers = {'mustache': _mustache_renderer(conn)}

    dry_run = conn['run']['dry']

    for result in fabsync.isync(conn, root, selector, renderers, dry_run=dry_run):
        print(f"{result.path}{' [modified]' if result.modified else ''}")
        if verbose > 0 and result.diff:
            print(result.diff.decode())
```

Of course you may also wish to save the results and use them to decide what
other actions to perform (e.g. restarting services).

Because we're just dealing with files, fabsync can offer a few other convenience
functions, including one that renders the source tree into human-readable rows.
If you rendered this with PrettyTable, it might look like this:

```
+-----------------------------------+------+-------+------------+----------+-------+--------+
| Path                              | User | Group | Mode       | Renderer | Diff? | Tags   |
+-----------------------------------+------+-------+------------+----------+-------+--------+
| /usr/                             |      |       |            |          |       |        |
| /usr/local/                       |      |       |            |          |       |        |
| /usr/local/etc/                   |      |       |            |          |       |        |
| /usr/local/etc/mail/              |      |       |            |          |       | mail   |
| /usr/local/etc/mail/smtpd.conf    |      |       |            |          |       | mail   |
| /usr/local/etc/rc.d/              | root | wheel |            |          |       |        |
| /usr/local/etc/rc.d/restic-server | root | wheel | -rwxr-xr-x |          |       | restic |
| /usr/local/etc/smb4.conf          |      |       |            |          |       |        |
| /usr/local/etc/wireguard/         |      |       | drwx------ |          |       | wg     |
| /usr/local/etc/wireguard/wg0.conf |      |       | -rw------- | mustache |       | wg     |
| /usr/local/utils/                 |      |       |            |          |       |        |
+-----------------------------------+------+-------+------------+----------+-------+--------+
```

Refer to the [documentation][] for more details and a step-by-step guide.

## Contributing

I wrote this for my own purposes and published it primarily to enforce the
discipline of comprehensive documentation and tests. It's deliberately narrow in
scope. New features are not out of the question, but mostly only those that
would be considerably more effort to implement externally.

Feel free to reach out with bug reports or suggestions. And note the Unlicense,
which means you can also just take the code and do what you like with it.

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>


[Fabric]: https://www.fabfile.org/
[documentation]: https://fabsync.ignorare.net/
