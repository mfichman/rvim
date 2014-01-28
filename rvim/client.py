#!/bin/env python

import httplib
import difflib
import urllib
import json
import sys
import subprocess
import shutil
import os
import json

class ClientException(Exception):
    pass

class Client:
    def __init__(self, host=None, port=None):
        self.host = host or os.environ['RVIMHOST']
        self.port = port or int(os.environ['RVIMPORT'])
        self.conn = httplib.HTTPConnection(host, port)

    def request(self, method, path, data=None):
        """
        Do a single rvim-server API request.
        """
        try:
            headers = {'Content-Type': 'application/json'} if data else {}
            self.conn.request(method, path, data, headers)
            response = self.conn.getresponse()
            if response.status == 404:
                raise ClientExcpetion('file not found')
            elif response.status != 200:
                raise ClientException(json.load(response)['status'])
            else:
                return response
        except httplib.HTTPException, e:
            self.conn.close()
            raise

    def file(self, path):
        """
        Get a file from the rvim-server by remote path name.
        """
        return self.request('GET', '/file/%s' % path).read()

    def patch(self, path, patch):
        """
        Post a patch to the rvim-server by remote path name.  The patch must be
        in unified diff format.
        """
        data = json.dumps({'path': path, 'patch': patch})
        return json.load(self.request('POST', '/patch', data))

    def next(self, id):
        """
        Wait for a file to open locally.  ID is the ID of the last file
        handled, or 0.
        """
        return json.load(self.request('GET', '/open/%d' % id))

    def open(self, path):
        """
        Request that a remote Vim open the file by remote path name.
        """
        data = json.dumps({'path': path})
        return json.load(self.request('POST', '/open', data))

def main():
    c = Client()
    id = 0
    while True:
        data = c.next(id)
        os.environ['RVIM'] = '1'
        os.environ['RVIMHOST'] = c.host
        os.environ['RVIMPORT'] = str(c.port)
        subprocess.Popen(('gvim', data['path']), shell=True)

if __name__ == '__main__':
    main()
