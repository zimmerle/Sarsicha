
try:
    from yaml import CLoader as Loader, CDumper as Dumper, load
except ImportError:
    from yaml import Loader, Dumper, load

import getopt, sys

from src.singleton import Singleton


DEFAULT_PROXY_CONFIGURATION = "default-proxy.yaml"
DEFAULT_NODE_CONFIGURATION = "default-node.yaml"


class Configuration(metaclass=Singleton):
    def __init__(self):
        self._conf = None
        self._loaded = False


    def load(self, f):
        try:
            with open(f, 'r') as content_file:
                content = content_file.read()
                self._conf = load(content)
            self._load = True
        except:
            raise


    def __getitem__(self, attr):
        a = attr.split(".")
        z = self._conf
        for i in a:
            z = z[i]
        return z


    def get(self):
        return self._conf


def usage():
    print ("   -c/--config=/path/to/file")
    print ("   \t\t Path to load the configuration file from.")


def _conf_name(f):
    import copy
    tmp = copy.deepcopy(sys.argv[1:])
    try:
        opts, args = getopt.getopt(tmp, "hc:", ["config=", "help"])
        for o, a in opts:
            if o in ("-o", "--output"):
                f = a
            elif o in ("-h", "--help"):
                usage()

    except getopt.GetoptError as err:
        pass
    return f


def loadProxyConfig():
    f = _conf_name(DEFAULT_PROXY_CONFIGURATION)    
    conf = Configuration()
    conf.load(f)

def loadNodeConfig():
    f = _conf_name(DEFAULT_NODE_CONFIGURATION)    
    conf = Configuration()
    conf.load(f)