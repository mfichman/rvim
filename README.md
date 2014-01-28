RVIM: Remote Editing for Vim
============================

RVIM is a plugin for remote Vim editing.  It runs a simple web app that serves
files and accepts patches to files.  The Vim plugin posts a "patch" to the web
server whenever the local copy of the file changes.  In addition, the plugin
lets you remote open files both from a remote shell and from within Vim itself.

Setup
-----

```
git clone https://github.com/mfichman/rvim.git
cd rim
python setup.py install
echo "au VimEnter * :py import rvim.vimplugin" >> ~/.vimrc
```

Your Vim must be compiled with `+python`.

Usage
-----

On the remote system, run:

```
cat > ~/.bashrc <<EOF
set RVIMHOST=<remote-host>
set RVIMPORT=<remote-port>
EOF
rvim-server
```

<font color='red'>**Warning**</font>: Do not run rvim-server on a public-facing
server, as it does not use authentication or SSH.  This may be improved in a
later version.  For now, restrict your usage of rvim-server to VPNs, etc.

On the local system, run:
```
set RVIMHOST=<remote-host>
set RVIMPORT=<remote-port>
rvim-client
```

To open a file locally, run:
```
RVIM=1 gvim /path/to/remote/file
```

To open a file remotely, but edit it locally in graphical Vim, run:
```
rvim /path/to/remote/file
```

This is useful for the situation where you have a remote shell open, but you still 
want to edit locally due to bandwidth constraints, or so that you can use graphical
Vim (yay for nice fonts and themes!) rather than the console.




