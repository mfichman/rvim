#!/bin/env python

import httplib
import urllib
import json
import sys
import os
import subprocess

class Cli:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = httplib.HTTPConnection(host, port)

    def open(self, path):
        # Post a patch to the server.
        data = json.dumps({'path': path})
        headers = {'Content-Type': 'application/json'}
        self.conn.request('POST', '/open', data, headers)
        response = self.conn.getresponse()
        data = json.load(response)
        if response.status != 200:
            sys.stderr.write('error: %s\n' % data['status'])
            sys.stderr.flush()
            sys.exit(1)
        return data

def main():
    c = Cli('localhost', 40000)  
    for arg in sys.argv[1:]:
        subprocess.Popen(('a4', 'edit', arg)).wait()
        c.open(os.path.abspath(arg))

if __name__ == '__main__':
    main()
