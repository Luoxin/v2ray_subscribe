import json
import traceback
from enum import Enum, unique


@unique
class ErrCode(Enum):
    Success = 0
    SystemError = -1  # 系统错误
    NetworkAnomaly = -2  # 网络异常
    ResponseParsingException = -3  # response解析异常


class Error:
    errcode = 0
    errmsg = "success"

    def __init__(self, errcode=0, errmsg="success"):
        if isinstance(errcode, ErrCode):
            self.set_with_errcode_class(errcode)
        elif isinstance(errcode, int):
            self.errcode = errcode
            self.errmsg = errmsg

    def set(self, errcode=0, errmsg="success"):
        if isinstance(errcode, ErrCode):
            self.set_with_errcode_class(errcode)
        elif isinstance(errcode, int):
            self.errcode = errcode
            self.errmsg = errmsg

        return self

    def set_errmsg(self, errmsg: (str, None, traceback)):
        if errmsg is not None:
            self.errmsg = errmsg

        return self

    def set_with_errcode_class(self, err_code_class: Enum = ErrCode.Success):
        if err_code_class is not None:
            self.errcode = err_code_class.value
            self.errmsg = err_code_class.name

        return self

    def is_success(self):
        return self.errcode == 0

    def is_error(self):
        return not self.is_success()

    def __repr__(self):
        return json.dumps({"errcode": self.errcode, "errmsg": self.errmsg})

    def __str__(self):
        return json.dumps({"errcode": self.errcode, "errmsg": self.errmsg})

    def __eq__(self, obj):
        if isinstance(obj, int):
            return self.errcode == obj
        elif isinstance(obj, Error):
            return self.errcode == obj.errcode
        elif isinstance(obj, dict):
            return (
                self.errcode == 0 if obj.get("errcode") is None else obj.get("errcode")
            )
        else:
            return self.errcode == 0
