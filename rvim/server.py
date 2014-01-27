#!/bin/env python

from gevent import monkey; monkey.patch_all()
import gevent.event
import bottle
import subprocess
import StringIO

pending = []
next_id = 0
event = gevent.event.Event()

@bottle.route('/file/<path:path>')
def file(path):
    # Handle a request from the client to download a whole file from the
    # server.  Open the file with a4, and then send the file down to the
    # client.
    return bottle.static_file(path, root='.')

@bottle.get('/open/<id:int>')
def open(id):
    # Wait for the next file to open.
    while len(pending) == 0 or pending[0]['id'] < id:
        event.wait(600)
    return pending.pop(0)

@bottle.post('/open')
def open():
    # Open a new file with the given name.
    global next_id
    path = bottle.request.json['path']
    data = {'id': next_id, 'path': path}
    pending.append(data)
    next_id += 1
    return data

@bottle.post('/patch')
def patch():
    # Post a diff of the given file and apply it.
    patch = bottle.request.json['patch']
    path = bottle.request.json['path']
    return {'status': 'success'}

def main():
    bottle.run(host='', port=40000, server='gevent', debug=True, reload=True)
      
if __name__ == '__main__':
    main()
