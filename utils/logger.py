import logging
import logging.handlers
import socket
import os
import sys
import platform

try:
    from conf.conf import LOG_DEBUG, SERVER_NAME, LOG_PATH
except ModuleNotFoundError:
    LOG_DEBUG = True
    SERVER_NAME = "test"
    LOG_PATH = "./test.log"

sys.path.append("../")

# 如果日志路径为空，根据系统来分别设置默认路径
if LOG_PATH == "":
    if platform.system() == "Windows":
        LOG_PATH = "C:/log"
    elif platform.system() == "Linux":
        LOG_PATH = "/home/log"
    # TODO 对于java平台的默认日志路径的处理
    else:
        sys.exit(-1)

log_config = {
    "debug": LOG_DEBUG,
    "log_path": LOG_PATH if LOG_PATH.endswith(".log") else "{}.log".format(LOG_PATH),
}

# print("日志输出路径", log_config["log_path"])

dir_path = os.path.dirname(LOG_PATH)
if not os.path.exists(dir_path) and LOG_DEBUG:
    os.makedirs(dir_path)
del dir_path


class Logger(logging.Logger):
    _instance = None
    _first = True
    # 什么时间什么级别在哪个模块的哪个文件的哪个方法 哪个行号做了什么事情
    formatter = logging.Formatter(
        "{} pid:%(process)d  level:%(levelname)s  ts:%(asctime)s  "
        "filename:%(filename)s  funcName:%(funcName)s  lineno: %(lineno)d  "
        "msg:%(message)s".format(SERVER_NAME)
    )

    def __init__(
        self,
        name=SERVER_NAME,
        debug=False,
        log_path=None,
        toaddrs=[],
        level=logging.INFO,
    ):
        """
        :param name: 日志管理器的名字
        """
        super().__init__(name, level)
        self._start = None
        self._end = None

        self.__initconf(debug, name, level)
        self.__inithandler(debug, log_path)

    def __initconf(self, debug, name, level):
        logging.Logger.__init__(self, name, logging.DEBUG if debug else level)

    def __inithandler(self, debug, log_path):
        self.__init_loghandler(debug, log_path)
        pass

    def __init_loghandler(self, debug, log_path):
        if debug:
            handler = logging.StreamHandler(sys.stdout)
        else:
            handler = logging.FileHandler(filename=log_path, encoding="utf-8")
        handler.setFormatter(self.formatter)
        self.addHandler(handler)


class PushLogger(logging.Logger):
    hostname = None
    _instance = None
    _first = True
    formatter = logging.Formatter("")
    _logger = Logger(
        name=SERVER_NAME, debug=log_config["debug"], log_path=log_config["log_path"],
    )

    def __init__(
        self,
        name="logger_push",
        debug=False,
        log_path=None,
        toaddrs=[],
        level=logging.INFO,
    ):
        """
        :param name: 日志管理器的名字
        """
        self._start = None
        self._end = None
        self.isDebug = debug
        self.__initconf(debug, name, level)
        self.__inithandler(debug, log_path, toaddrs)

    def __initconf(self, debug, name, level):
        logging.Logger.__init__(self, name, logging.DEBUG if debug else level)

    def __inithandler(self, debug, log_path, toaddres):
        self.__init_loghandler(debug, log_path)
        pass

    def __init_loghandler(self, debug, log_path):
        if debug:
            handler = logging.StreamHandler(sys.stdout)
        else:
            handler = logging.FileHandler(filename=log_path, encoding="utf-8")
        handler.setFormatter(self.formatter)
        self.addHandler(handler)

    def __to_string(self, *args, **kwargs):
        _msg = []
        for m in args:
            _msg.append("{}".format(m))
        return "\t".join(_msg)

    def notset(self, *msg):
        self._logger._log(logging.NOTSET, self.__to_string(*msg), None)

    def info(self, *msg):
        self._logger._log(logging.INFO, self.__to_string(*msg), None)

    def error(self, *msg):
        self._logger._log(logging.ERROR, self.__to_string(*msg), None)

    def warn(self, *msg):
        self._logger._log(logging.WARN, self.__to_string(*msg), None)

    def warning(self, *msg):
        self._logger._log(logging.WARNING, self.__to_string(*msg), None)

    def critical(self, *msg):
        self._logger._log(logging.CRITICAL, self.__to_string(*msg), None)

    def debug(self, *msg):
        if self.isDebug:
            self._logger._log(logging.DEBUG, self.__to_string(*msg), None)

    def get_sevhost(self):
        # 获取本机电脑名
        if not self.hostname:
            self.hostname = socket.gethostname()

        return self.hostname


logger = PushLogger(
    name=SERVER_NAME, debug=log_config["debug"], log_path=log_config["log_path"]
)
