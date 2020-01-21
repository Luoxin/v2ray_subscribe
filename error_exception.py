import yaml

from enum import Enum
from utils import logger  # 日志


# 错误的处理
class ErrorException:
    def __init__(self):
        self.code_to_msg = {}

    def get_errmsg_by_errcode(self, errcode: "int = 0") -> str:
        if self.code_to_msg.get(errcode) is not None:
            return self.code_to_msg.get(errcode)
        else:
            return "system error"

    def add_errmsg_by_errcode(self, errcode: "int = 0", errmsg: str != "") -> bool:
        try:
            if self.code_to_msg.get(errcode) is None:
                logger.warning("err: add errmsg fail {} {}".format(errcode, errmsg))
                return False
            else:
                self.code_to_msg[errcode] = errmsg
                return True
        except:
            logger.warning("err: add errmsg fail {} {}".format(errcode, errmsg))
            return False

    def register_error(self, errcode: "int = 0", errmsg: str != "") -> bool:
        try:
            if errcode not in self.code_to_msg.keys():
                if self.add_errmsg_by_errcode(errcode, errmsg):
                    return True

            logger.warning("err: register_error {} {}".format(errcode, errmsg))
            return False
        except:
            logger.warning("err: register_error {} {}".format(errcode, errmsg))
            return False

    def register_error_by_enum(self):
        pass


class ErrorEnum(Enum):
    def __init__(self):
        y = yaml.load(open("", "r"))
        if y.get("ErrorEnum") is not None:
            error_enum_map = y.get("ErrorEnum")
            if isinstance(error_enum_map, dict):
                for key, value in error_enum_map.keys():
                    pass


errHeader = ErrorException()
errHeader.register_error_by_enum()


class InternalException(Exception):
    pass


def create_error(errcode: int != 0):
    errmsg = errHeader.get_errmsg_by_errcode(errcode)
    create_error_with_msg(errcode, errmsg)


def create_error_with_msg(errcode: int != 0, errmsg: str != ""):
    raise InternalException(errcode, Instrument.encode_to_utf8(errmsg))
