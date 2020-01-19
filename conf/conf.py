import os
import yaml
from fake_useragent import UserAgent

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
    try:
        return s.get(key)
    except:
        return None


def get_conf_int(key):
    try:
        return int(get_conf(key))
    except:
        return 0


def get_conf_float(key):
    try:
        return float(get_conf(key))
    except:
        return 0.0


def get_conf_bool(key):
    try:
        return bool(get_conf(key))
    except:
        return False


user_agent = UserAgent()
