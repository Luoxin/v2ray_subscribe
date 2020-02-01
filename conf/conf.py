import json
import os
import traceback

import yaml


class VariableManagerException(Exception):
    """variable manager base exception"""


class LoadFileNotFound(FileNotFoundError, VariableManagerException):
    """load file is not exist"""


class InvalidConfigurationFile(VariableManagerException, yaml.scanner.ScannerError):
    """Invalid configuration file"""


class UnsupportedConfigurationFileTypes(VariableManagerException):
    """Unsupported configuration file types"""


class VariableManager(object):
    _supported_file_types = ["yaml"]

    def __init__(self, load_file=False, file_type: str = "yaml"):
        self.load_file_path = ""
        self._variable = None
        self.file_type = ""
        if load_file:
            self.reload_file(load_file=load_file, file_type=file_type)

    def set_conf(self, key: str, value):
        self._variable[key] = value

    def set_load_file(self, load_file=False, file_type: str = "yaml"):
        """
        :param file_type: 如果加载文件有效，此变量才生效，默认yaml，其他类型正在添加支持
        :param load_file: 如果不传入，默认不加载文件，如果传入
                            如果传入True，使用默认路径加载文件
                            如果传入指定路径，使用指定路径加载文件
        """
        if isinstance(load_file, bool):
            if load_file:
                self.load_file_path = _get_conf_file_path()
            else:
                return
        elif isinstance(load_file, str):
            self.load_file_path = load_file

        self.set_load_file_type(file_type=file_type)

    def set_load_file_type(self, file_type: str = "yaml"):
        """
        :param file_type: 如果加载文件有效，此变量才生效，默认yaml，其他类型正在添加支持
        :return:
        """
        if file_type not in self._supported_file_types:
            raise UnsupportedConfigurationFileTypes()
        self.file_type = file_type

    def reload_file(self, load_file=False, file_type: str = "yaml"):
        self.set_load_file(load_file=load_file, file_type=file_type)

        # 先判断配置文件是否存在，后期做默认配置
        if not os.path.exists(self.load_file_path):
            raise FileNotFoundError()

        if self.file_type == "yaml":
            try:
                with open(self.load_file_path, encoding="utf-8") as f:
                    self._variable = yaml.load(f, Loader=yaml.FullLoader)
            except yaml.scanner.ScannerError:
                traceback.print_exc()
                raise InvalidConfigurationFile()
        else:
            raise UnsupportedConfigurationFileTypes()

    def get_conf(self, key):
        try:
            return self._variable.get(key)
        except:
            return None

    def get_conf_str(self, key, default: str = ""):
        try:
            value = self.get_conf(key)
            return str(value) if value is not None else default
        except:
            return default

    def get_conf_int(self, key, default: int = 0):
        try:
            value = self.get_conf(key)
            return int(value) if value is not None else default
        except:
            return default

    def get_conf_float(self, key, default: float = 0.0):
        try:
            value = self.get_conf(key)
            return float(value) if value is not None else default
        except:
            return default

    def get_conf_bool(self, key, default: bool = False):
        try:
            value = self.get_conf(key)
            return bool(value) if value is not None else default
        except:
            return default

    def get_conf_dict(self, key, default: dict = None):
        if default is None:
            default = {}
        try:
            value = self.get_conf(key)
            return dict(value) if value is not None else default
        except:
            return default

    def get_conf_json(self, key, default: dict = None):
        if default is None:
            default = {}
        try:
            value = self.get_conf(key)
            return json.loads(value) if value is not None else default
        except:
            return default

    def get_conf_list(self, key, default: list = None):
        if default is None:
            default = []
        try:
            value = self.get_conf(key)
            return list(value) if value is not None else default
        except:
            return default


def _get_conf_file_path() -> str:
    conf_path_list = [
        str(os.path.abspath(os.path.dirname(__file__)) + "\conf.yaml").replace(
            "\\", "/"
        ),
        str(os.path.abspath(os.getcwd() + "\conf.yaml")).replace("\\", "/"),
        os.path.abspath(os.path.dirname(os.getcwd())).replace("\\", "/"),
    ]

    for conf_path in conf_path_list:
        if os.path.exists(conf_path):
            return conf_path

    print("无法找到配置文件 {}".format(conf_path_list))
    os._exit(-1)



if __name__ == "__main__":
    tmp = VariableManager(load_file=True)
    print(tmp.get_conf_bool("A"))
