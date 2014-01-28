#!/bin/env python

import rvim

def main():
    c = rvim.Client()
    for arg in sys.argv[1:]:
        try:
            c.open(os.path.abspath(arg))
        except rvim.Exception, e:
            sys.stderr.write('error: %s\n' % e.msg)
            sys.stderr.flush()
            sys.exit(1)
            

if __name__ == '__main__':
    main()
