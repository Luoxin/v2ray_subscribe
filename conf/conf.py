import os
import yaml
import traceback

from fake_useragent import UserAgent

s = None


def _get_conf_file_path() -> str:
    conf_path_list = [
        str(os.path.abspath(os.path.dirname(__file__)) + "\conf.yaml").replace(
            "\\", "/"
        ),
        str(os.path.abspath(os.getcwd())).replace("\\", "/"),
        os.path.abspath(os.path.dirname(os.getcwd())).replace("\\", "/"),
    ]

    for conf_path in conf_path_list:
        if os.path.exists(conf_path):
            return conf_path

    print("无法找到配置文件 {}".format(conf_path_list))
    os._exit(-1)


def init_conf(filename=_get_conf_file_path()):
    try:
        global s
        f = open(filename, encoding="utf-8")
        s = yaml.load(f, Loader=yaml.FullLoader)
        return True
    except yaml.scanner.ScannerError:
        print("Parse yaml file failed")
        traceback.print_exc()
        return False
    except:
        traceback.print_exc()
        return False


def init_state(filename=_get_conf_file_path()):
    return init_conf(filename=filename)


def get_conf(key):
    global s
    try:
        return s.get(key)
    except:
        return None


def get_conf_int(key):
    try:
        value = get_conf(key)
        return int(value) if value is not None else 0
    except:
        return 0


def get_conf_float(key):
    try:
        value = get_conf(key)
        return float(value) if value is not None else 0
    except:
        return 0.0


def get_conf_bool(key, default: bool = False):
    try:
        value = get_conf(key)
        return bool(value) if value is not None else default
    except:
        return default


if not init_conf():
    raise Exception("can not read conf file")

user_agent = UserAgent()

if __name__ == "__main__":
    print(get_conf("DB_URL"))
    # print("***获取当前目录***")
    # print(os.getcwd())
    # print(os.path.abspath(os.path.dirname(__file__)))
    #
    # print("***获取上级目录***")
    # print(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
    # print(os.path.abspath(os.path.dirname(os.getcwd())))
    # print(os.path.abspath(os.path.join(os.getcwd(), "..")))
    #
    # print("***获取上上级目录***")
    # print(os.path.abspath(os.path.join(os.getcwd(), "../..")))
