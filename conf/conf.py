import os
import yaml

s = None


def init_conf(filename=os.path.abspath(os.path.dirname(__file__)) + "\conf.yaml"):
    try:
        global s
        f = open(filename, encoding="utf-8")
        s = yaml.load(f, Loader=yaml.FullLoader)
        return True
    except:
        return False


init_conf()


def init_state(filename=os.path.abspath(os.path.dirname(__file__)) + "\conf.yaml"):
    return init_conf(filename=filename)


def get_conf(key):
    global s
    return s.get(key)
