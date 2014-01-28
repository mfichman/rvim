#!/bin/env python
import rvim
import vim
import os
import re
import threading
import difflib


data_path = os.path.join(os.path.expanduser('~'), '.rvimdata')

def main():
    # Entrypoint for the vim plugin
    global client
    host = os.environ['RVIMHOST']
    port = int(os.environ['RVIMPORT'])
    client = rvim.Client(host, port)
    vim.command('au BufReadCmd * :py rvim.vimplugin.buf_read_cmd()')
    vim.command('au BufWriteCmd * :py rvim.vimplugin.buf_write_cmd()')
    buf_read_cmd()

def write(path, data):
    # Write a file to the disk, and create any directories necessary.
    (dirname, _) = os.path.split(path)
    try:
        os.makedirs(dirname)
    except OSError:
        pass
    with open(path, 'w') as fd:
        fd.write(data)

def read(path):
    # Read a file from disk; throw an IOError if the file cannot be read.
    with open(path) as fd:
        return fd.read()

def remote_file_path(path):
    # Convert a local file path to a remote one.  
    path = path.replace(data_path, '')
    path = path.replace('\\', '/')
    return path

def local_file_path(path):
    path = path.replace(data_path, '')
    path = re.sub(r"^[A-Z]:\\", '', path)
    path = os.path.join(data_path, path)
    return path

def buf_read_cmd():
    # Read the file from the server
    if vim.current.buffer.name:
        path = local_file_path(vim.current.buffer.name)
        data = client.file(remote_file_path(path))
        try:
            os.remove(path)
        except OSError, e:
            pass
        write('%s.base' % path, data)
        vim.current.buffer[:] = data.split('\n')
        vim.current.buffer.name = path
        vim.command('set nomodified')
    
def buf_write_cmd():
    # Save diff of the current file to the server
    path = vim.current.buffer.name
    data = '\n'.join(vim.current.buffer)+'\n'
    write(path, data)
    new = data.splitlines(True)
    base = read('%s.base' % path).splitlines(True)
    patch = ''.join(difflib.unified_diff(base, new))
    if patch:
        client.patch(remote_file_path(path), patch) 
        write('%s.base' % path, data)
    vim.command('set nomodified')

if 'RVIM' in os.environ:
    main()

