RVIM: Remote Editing for Vim
============================

RVIM is a plugin for remote Vim editing.  It runs a simple web app that serves
files and accepts patches to files.  The Vim plugin posts a "patch" to the web
server whenever the local copy of the file changes.  In addition, the plugin
lets you remote open files both from a remote shell and from within Vim itself.

Setup
-----

To setup, download this repo and then run `python setup.py install`.  Edit your
~/.vimrc to include this line:

```
au VimEnter * :py import rvim.vimplugin
```

Your Vim must be compiled with `+python`.

Usage
-----

On the remote system, run `rvim-server`.  <font
color='red'>**Warning**</font>: Do not run rvim-server on a public-facing
server, as it does not use authentication or SSH.  This may be improved in a
later version.  For now, restrict your usage of rvim-server to VPNs, etc.

On both your local and remote system, set the following environment variables
in your shell:

```
set RVIMHOST=<remote-host>
set RVIMPORT=<remote-port>
```

Then, run `RVIM=1 gvim /path/to/remote/file` on your local system.
Alternatively, you can run `rvim-client <remote-host>:<remote-port>` on your
local system, and then run `rvim /path/to/remote/file` on your remote system. 



