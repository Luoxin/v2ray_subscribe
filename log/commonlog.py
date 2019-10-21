import logging
import logging.handlers
import socket
import sys

# import coloredlogs
sys.path.append('../')
# coloredlogs.auto_install()


class Logger(logging.Logger):
    _instance = None
    _first = True
    # 什么时间什么级别在哪个模块的哪个文件的哪个方法 哪个行号做了什么事情
    formatter = logging.Formatter('pid: %(process)d  level: %(levelname)s  ts: %(asctime)s  '
                                  'filename: %(filename)s  module: %(module)s  method: '
                                  '%(funcName)s  lineno: %(lineno)d  msg:%(message)s')

    def __init__(self, name='logger', debug=False, log_path=None, toaddrs=[], level=logging.INFO):
        '''
        :param name: 日志管理器的名字
        '''
        self._start = None
        self._end = None

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


from log.settings import LOGCONFIG as settings


class PushLogger(logging.Logger):
    hostname = None
    _instance = None
    _first = True
    formatter = logging.Formatter('')
    _logger = Logger(name=settings['name'], debug=settings['debug'], log_path=settings['log_path'], )

    def __init__(self, name='logger_push', debug=False, log_path=None, toaddrs=[], level=logging.INFO):
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
            handler = logging.FileHandler(filename=log_path, encoding="utf-8", )
        handler.setFormatter(self.formatter)
        self.addHandler(handler)

    def __to_string(self, *args, **kwargs):
        _msg = []
        for m in args:
            _msg.append('{}'.format(m))
        return '\t'.join(_msg)

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


logger = PushLogger(name=settings['name'], debug=settings['debug'], log_path=settings['log_path'])
