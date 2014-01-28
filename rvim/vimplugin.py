#!/bin/env python
import rvim
import vim
import os
import re
import threading
import difflib

def main():
    # Entrypoint for the vim plugin
    global client
    host = os.environ['RVIMHOST']
    port = int(os.environ['RVIMPORT'])
    client = rvim.Client(host, port)
    vim.command('au BufReadCmd * :py rvim.vimplugin.buf_read_cmd()')
    vim.command('au BufWriteCmd * :py rvim.vimplugin.buf_write_cmd()')

    th = threading.Thread(target=client.run)
    th.daemon = True
    th.start()
    buf_read_cmd()

def write(path, data):
    # Write a file to the disk, and create any directories necessary.
    path = os.path.join(os.path.expanduser('~'), '.data', path)
    (dirname, _) = os.path.split(path)
    try:
        os.makedirs(dirname)
    except OSError:
        pass
    with open(path, 'w') as fd:
        fd.write(data)

def read(path):
    # Read a file from disk; throw an IOError if the file cannot be read.
    path = os.path.join('.data', path)
    with open(path) as fd:
        return fd.read()

def remote_file_path(path):
    # Convert a local file path to a remote one.  
    cwd = os.getcwd()
    path = path.replace('%s\\' % cwd, '')
    path = re.sub(r'\\', '/', path)
    path = re.sub(r"^[A-Z]:/", '', path)
    return path 

def buf_read_cmd():
    # Read the file from the server
    path = remote_file_path(vim.current.buffer.name)
    data = client.file(path)
    vim.current.buffer[:] = data.split('\n')
    write('%s.base' % path, data)
    write(path, data)
    vim.command('set nomodified')
    
def buf_write_cmd():
    # Save diff of the current file to the server
    path = remote_file_path(vim.current.buffer.name)
    data = '\n'.join(vim.current.buffer)+'\n'
    write(path, data)
    new = data.splitlines(True)
    base = read('%s.base' % path).splitlines(True)

    patch = ''.join(difflib.unified_diff(base, new))
    if patch:
        client.patch(path, patch) 
    write('%s.base' % path, data)
    vim.command('set nomodified')

if 'RVIM' in os.environ:
    main()

